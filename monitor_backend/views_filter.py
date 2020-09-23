from django.shortcuts import HttpResponse
import django.views.decorators.http as dj_http
import requests
import json
import traceback
from docker import Client as dockerClient
from io import BytesIO

from monitor_backend.views_commons import logger, mydb_client


@dj_http.require_GET
def filter_list(req):
    res = {"status": "OK", "data": []}

    sql_list_filter = '''SELECT `sink_sources`.`id`, `sink_sources`.`name`,
                           `sink_sources`.`source_data_system`, `sink_sources`.`source_info`,
                           `n2n`.`id` as `n2n_id`, `n2n`.`name` as `n2n_name`,
                           `n2n`.`vlan_addr` as `vlan_addr`, `sink_sources`.`docker_port`,
                           `sink_sources`.`state`
                    FROM `sink_sources` JOIN `n2n` ON `sink_sources`.`n2n_id`=`n2n`.`id`
                    WHERE `sink_sources`.`role` = 'source' '''
    try:
        mydb_cursor.execute(sql_list_filter)
        for fil in mydb_cursor:
            res["data"].append({
                "id": fil[0],
                "name": fil[1],
                "source_data_system": fil[2],
                "source_info": fil[3],
                "n2n_id": fil[4],
                "n2n_name": fil[5],
                "vlan_addr": fil[6],
                "docker_port": fil[7],
                "state": fil[8]
            })
    except Exception as e:
        logger.error("List filters query [{}] failed: [{}]".format(
            sql_list_filter, e))
        res["status"] = "List filters query failed: [{}]".format(e)

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_POST
def filter_pull_image(req):
    res = {"status": "OK"}

    post_body = req.body.decode("UTF-8")
    try:
        post_data = json.loads(post_body)
    except Exception as e:
        post_data = {}

    if("image_name" in post_data and "tag" in post_data and
       "source_id" in post_data and "source_vlan_addr" in post_data
       and "docker_port" in post_data):

        try:
            docker_client = dockerClient(
                base_url="tcp://{}:{}".format(post_data["source_vlan_addr"],
                                              post_data["docker_port"]))
            docker_resp = docker_client.pull(
                "{}:{}/{}".format(post_data["image_name"]),
                tag=post_data["tag"], stream=True)
            for line in docker_resp:
                logger.info(line.decode('UTF-8'))
        except Exception as e:
            errmsg = "{} docker pull image {} failed: [{}]".format(
                post_data["source_vlan_addr"], post_data["image_name"], e)
            logger.error(errmsg)
            res["status"] = errmsg
    else:
        res["status"] = "miss parameter"

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_GET
def filter_source_images(req):
    res = {"status": "OK", "data": []}

    post_param = req.GET

    source_vlan_addr = post_param.get("source_vlan_addr")
    docker_port = post_param.get("docker_port")

    if(source_vlan_addr and docker_port):
        try:
            docker_client = dockerClient(
                base_url="tcp://{}:{}".format(source_vlan_addr, docker_port))
            docker_resp = docker_client.images()
            for line in docker_resp:
                res["data"].append(line["RepoTags"])
                logger.info(line["RepoTags"])
        except Exception as e:
            errmsg = "{} docker get image info failed: [{}]".format(
                source_vlan_addr, e)
            logger.error(errmsg)
            res["status"] = errmsg
    else:
        res["status"] = "miss parameter"

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_GET
def filter_create_container(req):
    res = {"status": "OK"}

    post_param = req.GET

    source_vlan_addr = post_param.get("source_vlan_addr")
    docker_port = post_param.get("docker_port")
    image_name_and_tag = post_param.get("image_name")
    container_name = post_param.get("container_name")

    if(source_vlan_addr and docker_port and
       image_name_and_tag and container_name):
        try:
            docker_client = dockerClient(
                base_url="tcp://{}:{}".format(source_vlan_addr, docker_port))
            docker_resp = docker_client.create_container(
                image=image_name_and_tag,
                name=container_name
            )
            logger.info(docker_resp)
        except Exception as e:
            errmsg = "create docker {} on {} get image info failed: [{}]".format(
                container_name, source_vlan_addr, e)
            logger.error(errmsg)
            res["status"] = errmsg
    else:
        res["status"] = "miss parameter"

    return HttpResponse(json.dumps(res), content_type="application/json")
