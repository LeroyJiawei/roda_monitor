from django.shortcuts import HttpResponse
from configparser import ConfigParser
import mysql.connector
import django.views.decorators.http as dj_http
import requests
import json
import logging
import traceback

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s - %(name)s] - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

cfg = ConfigParser()
cfg.read('config.ini')
mysql_host = cfg.get('mysql', 'host')
mysql_port = cfg.get('mysql', 'port')
mysql_user = cfg.get('mysql', 'username')
mysql_passwd = cfg.get('mysql', 'passwd')
mysql_db = cfg.get('mysql', 'database')

mydb_client = mysql.connector.connect(
    host=mysql_host,
    port=mysql_port,
    user=mysql_user,
    passwd=mysql_passwd,
    database=mysql_db
)
mydb_cursor = mydb_client.cursor()


@dj_http.require_POST
def n2n_registry(request):
    res = {"status": "OK"}

    # get post body json data
    post_data = json.loads(request.body.decode("UTF-8"))

    if ('role' in post_data and
        'vlan_addr' in post_data and
        'vlan_name' in post_data and
        'port' in post_data and
        'supernode_name' in post_data and
            'name' in post_data):

        # TODO: before insert should check whether current new n2n is unique
        sql_query = '''insert into n2n 
                    (`name`, `role`, `vlan_addr`, `port`, `supernode_name`, `vlan_name`, 
                        `key`, `create_time`, `update_time`, `state`, `description`) 
                    values 
                    ('{}','{}', '{}', '{}', '{}', '{}', 
                        '{}', now(), now(), 'init','{}')'''.format(
            post_data['name'], post_data['role'], post_data['vlan_addr'],
            post_data['port'], post_data['supernode_name'], post_data['vlan_name'],
            post_data['key'] if 'key' in post_data else 'null',
            post_data['description'] if 'description' in post_data else 'null')

        try:
            mydb_cursor.execute(sql_query)
            mydb_client.commit()
        except Exception as e:
            mydb_client.rollback()
            logger.error("Insert query [{}] failed: {}".format(sql_query, e))
            res["status"] = "mysql insert failed: {}".format(e)
    else:
        res["status"] = "miss parameter"
        return HttpResponse(json.dumps(res))

    return HttpResponse(json.dumps(res))


@dj_http.require_POST
def n2n_update(request):
    res = {"status": "OK"}

    # get post body json data
    post_data = json.loads(request.body.decode("UTF-8"))

    if ('id' in post_data and
        'role' in post_data and
        'vlan_addr' in post_data and
        'vlan_name' in post_data and
        'port' in post_data and
        'supernode_name' in post_data and
            'name' in post_data):

        # TODO: if it is changing the addr and port of supernode,
        # should change all relative edge nodes
        sql_query = '''update n2n set
                    `name` = '{}', `vlan_addr`='{}', `port`='{}', 
                    `supernode_name`='{}', `vlan_name`='{}', `key`='{}', 
                    `update_time`=now(), `description`='{}' 
                    where id={}
                    '''.format(
            post_data['name'], post_data['vlan_addr'],
            post_data['port'], post_data['supernode_name'], post_data['vlan_name'],
            post_data['key'] if 'key' in post_data else 'null',
            post_data['description'] if 'description' in post_data else 'null',
            post_data['id'])

        try:
            mydb_cursor.execute(sql_query)
            mydb_client.commit()
        except Exception as e:
            mydb_client.rollback()
            logger.error("update query [{}] failed: {}".format(sql_query, e))
            res["status"] = "mysql update failed: {}".format(e)
    else:
        res["status"] = "miss parameter"
        return HttpResponse(json.dumps(res))

    return HttpResponse(json.dumps(res))


@dj_http.require_http_methods(["DELETE"])
def n2n_delete(request):
    res = {"status": "OK"}

    # get post body json data
    delete_data = json.loads(request.body.decode("UTF-8"))

    if('id' in delete_data and 'role' in delete_data):  # role is not used currently
        # TODO: if it is deleting supernode, should delete all relative edge nodes
        sql_query = '''delete from n2n where id = {}'''.format(
            delete_data['id'])

        try:
            mydb_cursor.execute(sql_query)
            mydb_client.commit()
        except Exception as e:
            mydb_client.rollback()
            logger.error("delete query [{}] failed: {}".format(sql_query, e))
            res["status"] = "mysql delete failed: {}".format(e)
    else:
        res["status"] = "miss parameter"
        return HttpResponse(json.dumps(res))

    return HttpResponse(json.dumps(res))


@dj_http.require_GET
def n2n_lists(request):
    res = {"status": "OK"}

    get_data = request.GET  # this is a QueryDict object

    # if role does not exist, get() retuen none
    if(get_data.get('role') in ["supernode", "edge"]):
        sql_query = '''select `id`,`role`,`name`,`vlan_addr`,`port`,`vlan_name`,`key`,
                        `supernode_name`,`create_time`,`update_time`,`state`,`description` 
                        from n2n where role = '{}' '''.format(
            get_data.get('role'))

        try:
            mydb_cursor.execute(sql_query)
            res['data'] = []
            for tup in mydb_cursor:
                res['data'].append({
                    "id": tup[0], "role": tup[1],
                    "name": tup[2], "vlan_addr": tup[3],
                    "port": tup[4], "vlan_name": tup[5],
                    "key": tup[6],   "supernode_name": tup[7],
                    "create_time": str(tup[8]),  "update_time": str(tup[9]),
                    "state": tup[10], "description": tup[11]
                })

        except Exception as e:
            logger.error("select query [{}] failed: {}".format(sql_query, e))
            res["status"] = "mysql select failed: {}".format(e)

    else:
        res["status"] = "miss parameter/wrong role parameter"
        return HttpResponse(json.dumps(res))

    return HttpResponse(json.dumps(res))


@dj_http.require_GET
def n2n_topo(request):
    res = {"status": "OK"}

    supernodes_name = []
    # if role does not exist, get() retuen none
    sql_query = '''select `name`,`id` from n2n where role = 'supernode' '''
    try:
        mydb_cursor.execute(sql_query)
        supernodes_name = mydb_cursor.fetchall()
    except Exception as e:
        logger.error("select query [{}] failed: {}".format(sql_query, e))
        res["status"] = "mysql update failed: {}".format(e)
        return HttpResponse(json.dumps(res))

    res["data"] = {"nodes": [], "edges": []}
    for node in supernodes_name:
        # add current supernode to res
        res["data"]["nodes"].append({
            "name": node[0],
            "id": node[1]
        })
        sql_query = "select `name`,`id` from n2n where supernode_name = '{}'".format(
            node[0])
        try:
            mydb_cursor.execute(sql_query)
            for edge in mydb_cursor:
                res["data"]["nodes"].append({
                    "name": edge[0],
                    "id": edge[1]
                })
                res["data"]["edges"].append({
                    "source": node[1],
                    "target": edge[1]
                })
        except Exception as e:
            logger.error("select query [{}] failed: {}".format(sql_query, e))
            res["status"] = "mysql update failed: {}".format(e)

    return HttpResponse(json.dumps(res))
