from django.shortcuts import HttpResponse
import django.views.decorators.http as dj_http
import requests
import json
import traceback

from monitor_backend.views_commons import logger, mydb_cursor, mydb_client


@dj_http.require_POST
def sink_source_registry(request):
    res = {"status": "OK"}

    # get post body json data
    post_data = json.loads(request.body.decode("UTF-8"))

    if ('role' in post_data and 'name' in post_data and
            'n2n_id' in post_data and 'source_data_system' in post_data
            and 'source_info' in post_data and 'docker_port' in post_data):
        sql_query = '''INSERT INTO sink_sources
                        (`n2n_id`, `role`, `name`, `create_time`,
                            `update_time`, `source_data_system`, `source_info`, 
                            `state`, `description`,`docker_port`)
                        VALUES
                        ( {}, "{}","{}",  now(), now(), "{}", "{}",'init', {}, {});'''.format(
            post_data['n2n_id'], post_data['role'], post_data['name'],
            post_data['source_data_system'], post_data['source_info'],
            "'{}'".format(post_data['description']
                          )if 'description' in post_data else 'null',
            post_data['docker_port'] if post_data['role'] != "sink" else 'null')

        try:
            mydb_cursor.execute(sql_query)
            mydb_client.commit()
        except Exception as e:
            mydb_client.rollback()
            logger.error(
                "Sink source system insert query [{}] failed: {}".format(sql_query, e))
            res["status"] = "Sink source system insert failed: {}".format(e)
    else:
        res["status"] = "miss parameter"
        return HttpResponse(json.dumps(res))

    return HttpResponse(json.dumps(res))


@dj_http.require_POST
def sink_source_update(request):
    res = {"status": "OK"}

    # get post body json data
    post_data = json.loads(request.body.decode("UTF-8"))

    if ('id' in post_data and 'name' in post_data and
            'n2n_id' in post_data and 'source_data_system' in post_data
            and 'source_info' in post_data and 'docker_port' in post_data):
        sql_query = '''UPDATE sink_sources SET
                    `name` = '{}', `n2n_id`='{}', 
                    `source_data_system`='{}', `source_info`='{}',
                    `update_time`=now(), `description`='{}', `docker_port`={} 
                    WHERE id={}
                    '''.format(
            post_data['name'], post_data['n2n_id'],
            post_data['source_data_system'], post_data['source_info'],
            post_data['description'] if 'description' in post_data else 'null',
            post_data['docker_port'] if post_data['role'] != "sink" else 'null',
            post_data['id'])

        try:
            mydb_cursor.execute(sql_query)
            mydb_client.commit()
        except Exception as e:
            mydb_client.rollback()
            logger.error(
                "Sink source system update query [{}] failed: {}".format(sql_query, e))
            res["status"] = "Sink source system update failed: {}".format(e)
    else:
        res["status"] = "miss parameter"
        return HttpResponse(json.dumps(res))

    return HttpResponse(json.dumps(res))


@dj_http.require_http_methods(["DELETE"])
def sink_source_delete(request):
    res = {"status": "OK"}

    # get post body json data
    delete_data = json.loads(request.body.decode("UTF-8"))

    if('id' in delete_data):
        sql_query = "DELETE FROM sink_sources WHERE id = {}".format(
            delete_data['id'])

        try:
            mydb_cursor.execute(sql_query)
            mydb_client.commit()
        except Exception as e:
            mydb_client.rollback()
            logger.error(
                "Sink source system delete query [{}] failed: {}".format(sql_query, e))
            res["status"] = "Sink source system delete failed: {}".format(e)
    else:
        res["status"] = "miss parameter"
        return HttpResponse(json.dumps(res))

    return HttpResponse(json.dumps(res))


@dj_http.require_GET
def sink_source_list(request):
    res = {"status": "OK"}

    get_data = request.GET  # this is a QueryDict object

    param = get_data.get("role")

    if(param != None):
        sql_query = '''SELECT `sink_sources`.`id`, `sink_sources`.`name`, `sink_sources`.`role`,
                           `sink_sources`.`source_data_system`, `sink_sources`.`source_info`,
                           `n2n`.`id` as `n2n_id`,`n2n`.`name` as `n2n_name`,
                           `sink_sources`.`create_time`, `sink_sources`.`update_time`, 
                           `sink_sources`.`state`, `sink_sources`.`description`,`sink_sources`.`docker_port`
                    FROM `sink_sources` JOIN `n2n` ON `sink_sources`.`n2n_id`=`n2n`.`id` '''

        if(param != "all"):
            sql_query += " WHERE `sink_sources`.`role` = '{}'".format(param)

        try:
            mydb_cursor.execute(sql_query)
            res['data'] = []
            for tup in mydb_cursor:
                res['data'].append({
                    "id": tup[0], "name": tup[1], "role": tup[2],
                    "source_data_system": tup[3], "source_info": tup[4],
                    "n2n_id": tup[5], "n2n_name": tup[6],
                    "create_time": str(tup[7]), "update_time": str(tup[8]),
                    "state": tup[9], "description": tup[10], "docker_port": tup[11]
                })

        except Exception as e:
            logger.error(
                "Sink source system select query [{}] failed: {}".format(sql_query, e))
            res["status"] = "Sink source system select failed: {}".format(e)
    else:
        res["status"] = "miss parameter"
        return HttpResponse(json.dumps(res))

    return HttpResponse(json.dumps(res))


@dj_http.require_GET
def sink_source_topo(request):
    res = {"status": "OK"}

    sink_sources = []
    sql_query = '''SELECT `name`,`id`,`role` FROM sink_sources '''
    try:
        mydb_cursor.execute(sql_query)
        sink_sources = mydb_cursor.fetchall()
    except Exception as e:
        logger.error(
            "Sink system query select query [{}] failed: {}".format(sql_query, e))
        res["status"] = "Sink system query update failed: {}".format(e)
        return HttpResponse(json.dumps(res))

    sources = []
    sinks = []
    for system in sink_sources:
        if(system[-1] == 'source'):  # role field
            sources.append({
                "name": system[0],
                "id": system[1]
            })
        else:
            sinks.append({
                "name": system[0],
                "id": system[1]
            })

    res["data"] = {"nodes": sinks + sources, "edges": []}
    if(len(sinks) == 1):
        for sour in sources:
            res["data"]["edges"].append({
                "source": sinks[0]["id"],  # id
                "target": sour["id"]  # id
            })

    return HttpResponse(json.dumps(res))
