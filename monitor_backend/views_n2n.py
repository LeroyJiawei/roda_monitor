from django.shortcuts import HttpResponse
import django.views.decorators.http as dj_http
import requests
import json
import traceback

from monitor_backend.views_commons import logger, mydb_cursor, mydb_client


@dj_http.require_POST
def n2n_registry(request):
    res = {"status": "OK"}

    # get post body json data
    post_data = json.loads(request.body.decode("UTF-8"))

    if ('role' in post_data and
        'vlan_addr' in post_data and
        'vlan_name' in post_data and
        'supernode_name' in post_data and
            'name' in post_data):

        # TODO: before insert should check whether current new n2n is unique
        sql_query = '''INSERT INTO n2n
                    (`name`, `role`, `vlan_addr`, `docker_port`, `service_port`,
                        `supernode_name`, `vlan_name`,
                        `key`, `create_time`, `update_time`, `state`, `description`, `addr` )
                    VALUES
                    ('{}','{}', '{}', '{}', '{}', {}, {}, 
                        {}, now(), now(), 'init',{},{})'''.format(
            post_data['name'], post_data['role'], post_data['vlan_addr'],
            post_data['supernode_name'], post_data['vlan_name'],
            "'{}'".format(post_data['docker_port']
                          ) if 'docker_port' in post_data else 'null',
            "'{}'".format(post_data['service_port']
                          ) if 'service_port' in post_data else 'null',
            "'{}'".format(post_data['key']
                          ) if 'key' in post_data else 'null',
            "'{}'".format(post_data['description']
                          ) if 'description' in post_data else 'null',
            "'{}'".format(post_data['addr']
                          ) if 'addr' in post_data else 'null'
        )

        try:
            mydb_cursor.execute(sql_query)
            mydb_client.commit()
        except Exception as e:
            mydb_client.rollback()
            logger.error(
                "N2N insert query [{}] failed: {}".format(sql_query, e))
            res["status"] = "N2N insert failed: {}".format(e)
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
        'supernode_name' in post_data and
            'name' in post_data):

        # TODO: if it is changing the addr and port of supernode,
        # should change all relative edge nodes
        sql_query = '''UPDATE n2n SET
                    `name` = '{}', `vlan_addr`='{}', `port`='{}',
                    `supernode_name`='{}', `vlan_name`='{}', `key`={},
                    `update_time`=now(), `description`={}, `service_port`={},
                    `docker_port`={}, `addr`={} 
                    WHERE id={}
                    '''.format(
            post_data['name'], post_data['vlan_addr'],
            post_data['port'], post_data['supernode_name'], post_data['vlan_name'],
            "'{}'".format(post_data['key']
                          ) if 'key' in post_data else 'null',
            "'{}'".format(post_data['description']
                          ) if 'description' in post_data else 'null',
            "'{}'".format(post_data['service_port']
                          ) if 'service_port' in post_data else 'null',
            "'{}'".format(post_data['docker_port']
                          ) if 'docker_port' in post_data else 'null',
            "'{}'".format(post_data['addr']
                          ) if 'addr' in post_data else 'null',
            post_data['id'])

        try:
            mydb_cursor.execute(sql_query)
            mydb_client.commit()
        except Exception as e:
            mydb_client.rollback()
            logger.error(
                "N2N update query [{}] failed: {}".format(sql_query, e))
            res["status"] = "N2N update failed: {}".format(e)
    else:
        res["status"] = "miss parameter"
        return HttpResponse(json.dumps(res))

    return HttpResponse(json.dumps(res))


@dj_http.require_http_methods(["DELETE"])
def n2n_delete(request):
    res = {"status": "OK"}

    # get post body json data
    delete_data = json.loads(request.body.decode("UTF-8"))

    if('id' in delete_data):
        # TODO: if it is deleting supernode, should delete all relative edge nodes
        sql_query = '''DELETE FROM n2n WHERE id = {}'''.format(
            delete_data['id'])

        try:
            mydb_cursor.execute(sql_query)
            mydb_client.commit()
        except Exception as e:
            mydb_client.rollback()
            logger.error(
                "N2N delete query [{}] failed: {}".format(sql_query, e))
            res["status"] = "N2N delete failed: {}".format(e)
    else:
        res["status"] = "miss parameter"
        return HttpResponse(json.dumps(res))

    return HttpResponse(json.dumps(res))


@dj_http.require_GET
def n2n_list(request):
    res = {"status": "OK"}

    get_data = request.GET  # this is a QueryDict object

    param = get_data.get('role')
    # if role does not exist, get() retuen none
    if(param):
        sql_query = '''SELECT `id`,`role`,`name`,`vlan_addr`,`docker_port`,`vlan_name`,`key`,
                        `supernode_name`,`create_time`,`update_time`,`state`,`description`,
                        `service_port`, `addr` 
                        FROM n2n '''
        if(param != "all"):
            sql_query += " WHERE role = '{}'".format(param)

        try:
            mydb_cursor.execute(sql_query)
            res['data'] = []
            for tup in mydb_cursor:
                res['data'].append({
                    "id": tup[0], "role": tup[1],
                    "name": tup[2], "vlan_addr": tup[3],
                    "docker_port": tup[4], "vlan_name": tup[5],
                    "key": tup[6],   "supernode_name": tup[7],
                    "create_time": str(tup[8]),  "update_time": str(tup[9]),
                    "state": tup[10], "description": tup[11],
                    "service_port": tup[12], "addr": tup[13]
                })

        except Exception as e:
            logger.error(
                "N2N select query [{}] failed: {}".format(sql_query, e))
            res["status"] = "N2N select failed: {}".format(e)

    else:
        res["status"] = "miss parameter"
        return HttpResponse(json.dumps(res))

    return HttpResponse(json.dumps(res))


@dj_http.require_GET
def n2n_topo(request):
    res = {"status": "OK"}

    supernodes_name = []
    # if role does not exist, get() retuen none
    sql_query = '''SELECT `name`,`id` FROM n2n WHERE role = 'supernode' '''
    try:
        mydb_cursor.execute(sql_query)
        supernodes_name = mydb_cursor.fetchall()
    except Exception as e:
        logger.error("N2N select query [{}] failed: {}".format(sql_query, e))
        res["status"] = "N2N select failed: {}".format(e)
        return HttpResponse(json.dumps(res))

    res["data"] = {"nodes": [], "edges": []}
    for node in supernodes_name:
        # add current supernode to res
        res["data"]["nodes"].append({
            "name": node[0],
            "id": node[1]
        })
        sql_query = "SELECT `name`,`id` FROM n2n WHERE supernode_name = '{}'".format(
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
            logger.error(
                "N2N select query [{}] failed: {}".format(sql_query, e))
            res["status"] = "N2N select failed: {}".format(e)

    return HttpResponse(json.dumps(res))
