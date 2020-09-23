from django.shortcuts import HttpResponse
import django.views.decorators.http as dj_http
import requests
import json
import traceback
from docker import Client as dockerClient
from io import BytesIO

from monitor_backend.views_commons import logger, mydb_client


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

    return HttpResponse(json.dumps(res), content_type="application/json")


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

            res["data"].append({
                "name": "{}:{}/{}".format(hub_addr[0], hub_addr[1], tag_list["name"]),
                "tags": tag_list["tags"]
            })
    except Exception as e:
        errmsg = "Get Hub repository tags failed: {}".format(e)
        logger.error(errmsg)
        res["status"] = errmsg

    return HttpResponse(json.dumps(res), content_type="application/json")


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

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_GET
def hub_list_docker_images(req):
    res = {"status": "OK"}

    sql_get_hub_addr = "select `vlan_addr` from `n2n` where `role` = 'hub-edge'"
    try:
        mydb_cursor.execute(sql_get_hub_addr)
        hub_addr = mydb_cursor.fetchone()
    except Exception as e:
        logger.error("Get Hub vlan addr query [{}] failed: [{}]".format(
            sql_get_hub_addr, e))
        res["status"] = "Get Hub vlan addr query failed: [{}]".format(e)
        return HttpResponse(json.dumps(res), content_type="application/json")

    try:
        docker_cli = dockerClient(
            base_url='tcp://{}:{}'.format(hub_addr[0], "2375"))
        res["data"] = docker_cli.images()
    except Exception as e:
        errmsg = "Get Hub docker engine images failed: [{}]".format(e)
        logger.error(errmsg)
        res["status"] = errmsg

    return HttpResponse(json.dumps(res), content_type="application/json")


# TODO, should have two ways to build a image:
#   1. default way and set transfered paramters
#   2. transfer a dockerfile
@dj_http.require_POST
def hub_build_docker_images(req):
    res = {"status": "OK"}

    dockerfile = '''
        FROM centos:7

        MAINTAINER xjw <xjw_titan@sjtu.edu.cn>

        # CMD "cp /root/imageBuild/jdk-11.0.7_linux-x64_bin.rpm . "

        # CMD "pwd"
        # ADD jdk-11.0.7_linux-x64_bin.rpm /root/

        # RUN rpm -ivh /root/jdk-11.0.7_linux-x64_bin.rpm

        # RUN java --version

        CMD "top"
        # ENV JAVA_HOME /usr/local/java/jdk-11.0.3
        # ENV PATH $JAVA_HOME/bin:$PATH

        # ENTRYPOINT ["java","-jar","/app.jar"]
    '''

    post_data = json.loads(req.body.decode("UTF-8"))
    if("name" in post_data):
        sql_get_hub_addr = "select `vlan_addr` from `n2n` where `role` = 'hub-edge'"
        try:
            mydb_cursor.execute(sql_get_hub_addr)
            hub_addr = mydb_cursor.fetchone()
        except Exception as e:
            logger.error("Get Hub vlan addr query [{}] failed: [{}]".format(
                sql_get_hub_addr, e))
            res["status"] = "Get Hub vlan addr query failed: [{}]".format(e)
            return HttpResponse(json.dumps(res), content_type="application/json")

        file_bytes = BytesIO(dockerfile.encode("UTF-8"))
        try:
            docker_client = dockerClient(
                base_url="tcp://{}:{}".format(hub_addr[0], "2375"))  # default 2375
            docker_resp = docker_client.build(
                fileobj=file_bytes, rm=True, tag="{}:{}".format(
                    post_data["name"],
                    post_data["tag"] if "tag" in post_data else "null"))
            for line in docker_resp:
                line_stream_info = line.decode("UTF-8")
                if("stream" not in line_stream_info):
                    errmsg = "Build new image '{}:{}' failed: {}".format(
                        post_data["name"],
                        post_data["tag"] if "tag" in post_data else "null",
                        line_stream_info)
                    logger.error(errmsg)
                    res["status"] = errmsg
                    break
            logger.info("Build new image '{}:{}' success".format(
                        post_data["name"],
                        post_data["tag"] if "tag" in post_data else "null"))

        except Exception as e:
            errmsg = "Build new image '{}:{}' failed: {}".format(
                post_data["name"],
                post_data["tag"] if "tag" in post_data else "null",
                e)
            logger.error(errmsg)
            res["status"] = errmsg
    else:
        res["status"] = "miss parameter"

    return HttpResponse(json.dumps(res), content_type="application/json")
