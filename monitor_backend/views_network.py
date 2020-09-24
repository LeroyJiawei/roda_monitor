from django.shortcuts import HttpResponse
import django.views.decorators.http as dj_http
import requests
import json
import traceback

import monitor_backend.views_commons as roda


@dj_http.require_GET
def network_is_overlay(req):
    res = {"status": "OK", "data": {}}

    sql_query = "SELECT `value` FROM `universe` WHERE `config_name`='is_overlay' "

    try:
        roda.mydb_cursor.execute(sql_query)
        resp = roda.mydb_cursor.fetchall()
        if(len(resp) >= 1 and len(resp[0]) >= 1):
            res["data"] = True if resp[0][0] != 0 else False
        else:
            res["status"] = "not indicated in database"

    except Exception as e:
        roda.logger.error(
            "network query [{}] failed: {}".format(sql_query, e))
        res["status"] = "network query failed: {}".format(e)

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_GET
def network_set_overlay(req):
    res = {"status": "OK"}

    get_data = req.GET
    target_value = get_data.get("value")

    if(target_value == "true" or target_value == "false"):
        value = target_value == "true"

        sql_query = "SELECT `id` FROM `network` WHERE `role` <> 'supernode' "\
            "AND `{}` is null ".format("vlan_addr" if value else "addr")
        try:
            roda.mydb_cursor.execute(sql_query)
            resp = roda.mydb_cursor.fetchall()
        except Exception as e:
            resp = []
            res["status"] = "failed to query {}".format(e)

        if(len(resp) != 0):
            res["status"] = "Cannot set, some components does not have {}addresses".format(
                "vlan " if value else "")
        else:
            sql_query = "UPDATE `universe` SET `value`={} WHERE "\
                "`config_name`='is_overlay' ".format(1 if value else 0)
            try:
                roda.mydb_cursor.execute(sql_query)
                roda.mydb_client.commit()
                roda.Is_overlay_network = value
            except Exception as e:
                roda.mydb_client.rollback()
                res["status"] = "failed to update {}".format(e)
    else:
        res["status"] = "miss parameter"

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_POST
def network_registry(req):
    res = {"status": "OK"}

    roda.logger.info(req.body)
    # get post body json data
    post_data = json.loads(req.body.decode("UTF-8"))

    if ('role' in post_data and
            'name' in post_data and
            'addr' in post_data and (
                not roda.Is_overlay_network or (
                    'vlan_addr' in post_data and
                    'vlan_name' in post_data and
                    'key' in post_data and
                    'supernode_name' in post_data
                )
            )):

        sql_query = '''INSERT INTO network
                        (`name`, `role`, `addr`, 
                        `vlan_addr`,`vlan_name`,`key`, `supernode_name`, 
                        `service_port`, `description`, 
                        `state`, `create_time`, `update_time`)
                    VALUES
                    ('{}','{}','{}',{},{},{},{},{},{},
                    'init',now(), now())'''.format(
            post_data['name'], post_data['role'], post_data['addr'],
            roda.current_val_or_null("vlan_addr", post_data, False),
            roda.current_val_or_null("vlan_name", post_data, False),
            roda.current_val_or_null("key", post_data, False),
            roda.current_val_or_null("supernode_name", post_data, False),
            roda.current_val_or_null("service_port", post_data, True),
            roda.current_val_or_null("description", post_data, False))

        try:
            roda.mydb_cursor.execute(sql_query)
            roda.mydb_client.commit()
        except Exception as e:
            roda.mydb_client.rollback()
            roda.logger.error(
                "network insert query [{}] failed: {}".format(sql_query, e))
            res["status"] = "network insert failed: {}".format(e)
    else:
        res["status"] = "miss parameter"
        return HttpResponse(json.dumps(res), content_type="application/json")

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_GET
def network_list(req):
    res = {"status": "OK"}

    get_data = req.GET  # this is a QueryDict object

    param = get_data.get('role')
    # if role does not exist, get() retuen none
    if(param):
        sql_query = '''SELECT `id`,`role`,`name`,`vlan_addr`,`vlan_name`,`key`,
                        `supernode_name`,`create_time`,`update_time`,`state`,
                        `description`, `service_port`, `addr` FROM network '''
        if(param != "all"):
            sql_query += " WHERE role = '{}'".format(param)

        try:
            roda.mydb_cursor.execute(sql_query)
            res['data'] = []
            for tup in roda.mydb_cursor:
                res['data'].append({
                    "id": tup[0], "role": tup[1],
                    "name": tup[2], "vlan_addr": tup[3],
                    "vlan_name": tup[4], "key": tup[5],
                    "supernode_name": tup[6],
                    "create_time": str(tup[7]),  "update_time": str(tup[8]),
                    "state": tup[9], "description": tup[10],
                    "service_port": tup[11], "addr": tup[12]
                })

        except Exception as e:
            roda.logger.error(
                "network select query [{}] failed: {}".format(sql_query, e))
            res["status"] = "network select failed: {}".format(e)

    else:
        res["status"] = "miss parameter"
        return HttpResponse(json.dumps(res), content_type="application/json")

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_POST
def network_update(req):
    res = {"status": "OK"}

    # get post body json data
    post_data = json.loads(req.body.decode("UTF-8"))

    if ('id' in post_data and
        'role' in post_data and
        'name' in post_data and
            'addr' in post_data and (
                not roda.Is_overlay_network or (
                    'vlan_addr' in post_data and
                    'vlan_name' in post_data and
                    'key' in post_data and
                    'supernode_name' in post_data
                )
            )):

        # TODO: if it is changing the addr and port of supernode,
        # should change all relative edge nodes
        sql_query = '''UPDATE network SET
                    `name` = '{}', `role`='{}', addr='{}', 
                    `vlan_addr`={}, `vlan_name`={}, `key`={},
                    `supernode_name`={}, `update_time`=now(), 
                    `description`={}, `service_port`={} WHERE id={}'''.format(
            post_data['name'], post_data['role'], post_data['addr'],
            roda.current_val_or_null("vlan_addr", post_data, False),
            roda.current_val_or_null("vlan_name", post_data, False),
            roda.current_val_or_null("key", post_data, False),
            roda.current_val_or_null("supernode_name", post_data, False),
            roda.current_val_or_null("description", post_data, False),
            roda.current_val_or_null("service_port", post_data, True),
            post_data['id'])

        try:
            roda.mydb_cursor.execute(sql_query)
            roda.mydb_client.commit()
        except Exception as e:
            roda.mydb_client.rollback()
            roda.logger.error(
                "network update query [{}] failed: {}".format(sql_query, e))
            res["status"] = "network update failed: {}".format(e)
    else:
        res["status"] = "miss parameter"
        return HttpResponse(json.dumps(res), content_type="application/json")

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_http_methods(["DELETE"])
def network_delete(req):
    res = {"status": "OK"}

    # get post body json data
    delete_data = json.loads(req.body.decode("UTF-8"))

    if('id' in delete_data):
        sql_query = '''DELETE FROM network WHERE id = {}'''.format(
            delete_data['id'])

        try:
            roda.mydb_cursor.execute(sql_query)
            roda.mydb_client.commit()
        except Exception as e:
            roda.mydb_client.rollback()
            roda.logger.error(
                "network delete query [{}] failed: {}".format(sql_query, e))
            res["status"] = "network delete failed: {}".format(e)
    else:
        res["status"] = "miss parameter"
        return HttpResponse(json.dumps(res), content_type="application/json")

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_GET
def network_topo(req):
    res = {"status": "OK"}

    supernodes_name = []
    # if role does not exist, get() retuen none
    sql_query = '''SELECT `name`,`id` FROM network WHERE role = 'supernode' '''
    try:
        roda.mydb_cursor.execute(sql_query)
        supernodes_name = roda.mydb_cursor.fetchall()
    except Exception as e:
        roda.logger.error(
            "network select query [{}] failed: {}".format(sql_query, e))
        res["status"] = "network select failed: {}".format(e)
        return HttpResponse(json.dumps(res), content_type="application/json")

    res["data"] = {"nodes": [], "edges": []}
    for node in supernodes_name:
        # add current supernode to res
        res["data"]["nodes"].append({
            "name": node[0],
            "id": node[1]
        })
        sql_query = "SELECT `name`,`id` FROM network WHERE supernode_name = '{}'".format(
            node[0])
        try:
            roda.mydb_cursor.execute(sql_query)
            for edge in roda.mydb_cursor:
                res["data"]["nodes"].append({
                    "name": edge[0],
                    "id": edge[1]
                })
                res["data"]["edges"].append({
                    "source": str(node[1]),
                    "target": str(edge[1])
                })
        except Exception as e:
            roda.logger.error(
                "network select query [{}] failed: {}".format(sql_query, e))
            res["status"] = "network select failed: {}".format(e)

    return HttpResponse(json.dumps(res), content_type="application/json")
