from django.shortcuts import HttpResponse
import django.views.decorators.http as dj_http
import requests
import json
import traceback

from monitor_backend.views_commons import logger, mydb_cursor, mydb_client


@dj_http.require_GET
def hub_info(req):
    res = {"status": "OK", "data": {}}

    sql_get_hub_addr = "select `vlan_addr`,`service_port` from `n2n` where `role` = 'hub-edge'"
    try:
        mydb_cursor.execute(sql_get_hub_addr)
        hub_addr = mydb_cursor.fetchone()
    except Exception as e:
        logger.error("Get Hub vlan addr query [{}] failed: [{}]".format(
            sql_get_hub_addr, e))
        res["status"] = "Get Hub vlan addr query failed: [{}]".format(e)

    res["data"] = {
        "vlan_addr": hub_addr[0],
        "port": hub_addr[1]
    }

    return HttpResponse(json.dumps(res))


@dj_http.require_GET
def hub_list_images(req):
    res = {"status": "OK", "data": []}

    sql_get_hub_addr = "select `vlan_addr`,`service_port` from `n2n` where `role` = 'hub-edge'"
    try:
        mydb_cursor.execute(sql_get_hub_addr)
        hub_addr = mydb_cursor.fetchone()
    except Exception as e:
        logger.error("Get Hub vlan addr query [{}] failed: [{}]".format(
            sql_get_hub_addr, e))
        res["status"] = "Get Hub vlan addr query failed: [{}]".format(e)

    try:
        hub_resp = requests.get(
            "http://{}:{}/v2/_catalog".format(hub_addr[0], hub_addr[1]))
        repo_list = hub_resp.json()["repositories"]

        for repo in repo_list:
            hub_resp = requests.get(
                "http://{}:{}/v2/{}/tags/list".format(hub_addr[0], hub_addr[1], repo))
            tag_list = hub_resp.json()

            res["data"].append(tag_list)
    except Exception as e:
        errmsg = "Get Hub repository tags failed: {}".format(e)
        logger.info(errmsg)
        res["status"] = errmsg

    return HttpResponse(json.dumps(res))


@dj_http.require_http_methods(["DELETE"])
def hub_delete_image(req):
    res = {"status": "OK"}

    delete_data = {}

    body_data = req.body.decode("UTF-8")
    if(body_data != ""):
        delete_data = json.loads(body_data)

    if('name' in delete_data and 'tag' in delete_data):

        sql_get_hub_addr = "select `vlan_addr`,`service_port` from `n2n` where `role` = 'hub-edge'"
        try:
            mydb_cursor.execute(sql_get_hub_addr)
            hub_addr = mydb_cursor.fetchone()
        except Exception as e:
            logger.error("Get Hub vlan addr query [{}] failed: [{}]".format(
                sql_get_hub_addr, e))
            res["status"] = "Get Hub vlan addr query failed: [{}]".format(e)

        try:
            hub_resp = requests.get(
                "http://{}:{}/v2/{}/manifests/{}".format(
                    hub_addr[0], hub_addr[1], delete_data["name"], delete_data["tag"]),
                headers={"Accept": "application/vnd.docker.distribution.manifest.v2+json"})
            image_digest = hub_resp.headers["Docker-Content-Digest"]
            logger.info(image_digest)
            hub_resp = requests.delete(
                "http://{}:{}/v2/{}/manifests/{}".format(hub_addr[0], hub_addr[1],
                                                         delete_data["name"], image_digest))
            if(hub_resp.status_code != 202):
                raise ValueError("Status Code of delete is not 202")

        except Exception as e:
            errmsg = "Delete Hub repository tags failed: {}".format(e)
            logger.error(errmsg)
            res["status"] = errmsg
    else:
        res["status"] = "mis parameter"

    return HttpResponse(json.dumps(res))
