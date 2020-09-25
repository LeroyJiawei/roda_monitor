from django.shortcuts import HttpResponse
import django.views.decorators.http as dj_http
import requests
import json
import traceback
import time
from docker import Client as dockerClient
from io import BytesIO
from influxdb import InfluxDBClient

import monitor_backend.views_commons as roda


@dj_http.require_GET
def filter_list(req):
    res = {"status": "OK", "data": []}

    sql_list_filter = "SELECT `sink_sources`.`id`, `sink_sources`.`name`,"\
        " `sink_sources`.`source_data_system`, `sink_sources`.`source_info`,"\
        " `network`.`id` as `network_id`, `network`.`name` as `network_name`,"\
        " `network`.`vlan_addr` as `vlan_addr`, `sink_sources`.`docker_port`,"\
        " `sink_sources`.`state`,`network`.`addr` as `addr` "\
        " FROM `sink_sources` JOIN `network` ON `sink_sources`.`network_id`=`network`.`id`"\
        " WHERE `sink_sources`.`role` = 'source' "
    try:
        roda.mydb_cursor.execute(sql_list_filter)
        for fil in roda.mydb_cursor:
            res["data"].append({
                "id": fil[0],
                "name": fil[1],
                "source_data_system": fil[2],
                "source_info": fil[3],
                "network_id": fil[4],
                "network_name": fil[5],
                "vlan_addr": fil[6],
                "docker_port": fil[7],
                "state": fil[8],
                "addr": fil[9],
            })
    except Exception as e:
        roda.logger.error("List filters query [{}] failed: [{}]".format(
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
       "source_id" in post_data and "source_addr" in post_data
       and "docker_port" in post_data):

        try:
            docker_client = dockerClient(
                base_url="tcp://{}:{}".format(post_data["source_addr"],
                                              post_data["docker_port"]))
            docker_resp = docker_client.pull(
                "{}:{}/{}".format(post_data["image_name"]),
                tag=post_data["tag"], stream=True)
            for line in docker_resp:
                roda.logger.info(line.decode('UTF-8'))
        except Exception as e:
            errmsg = "{} docker pull image {} failed: [{}]".format(
                post_data["source_addr"], post_data["image_name"], e)
            roda.logger.error(errmsg)
            res["status"] = errmsg
    else:
        res["status"] = "miss parameter"

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_GET
def filter_source_images(req):
    res = {"status": "OK", "data": []}

    post_param = req.GET

    source_addr = post_param.get("source_addr")
    docker_port = post_param.get("docker_port")

    if(source_addr and docker_port):
        try:
            docker_client = dockerClient(
                base_url="tcp://{}:{}".format(source_addr, docker_port))
            docker_resp = docker_client.images()
            for line in docker_resp:
                res["data"].append(line["RepoTags"])
                roda.logger.info(line["RepoTags"])
        except Exception as e:
            errmsg = "{} docker get image info failed: [{}]".format(
                source_addr, e)
            roda.logger.error(errmsg)
            res["status"] = errmsg
    else:
        res["status"] = "miss parameter"

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_GET
def filter_create_container(req):
    res = {"status": "OK"}

    post_param = req.GET

    source_addr = post_param.get("source_addr")
    docker_port = post_param.get("docker_port")
    image_name_and_tag = post_param.get("image_name")
    container_name = post_param.get("container_name")

    if(source_addr and docker_port and
       image_name_and_tag and container_name):
        try:
            docker_client = dockerClient(
                base_url="tcp://{}:{}".format(source_addr, docker_port))
            docker_resp = docker_client.create_container(
                image=image_name_and_tag,
                name=container_name
            )
            roda.logger.info(docker_resp)
        except Exception as e:
            errmsg = "create docker {} on {} get image info failed: [{}]".format(
                container_name, source_addr, e)
            roda.logger.error(errmsg)
            res["status"] = errmsg
    else:
        res["status"] = "miss parameter"

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_GET
def filter_get_match_perf(req):
    res = {"status": "OK"}

    filter_id = req.GET.get("filter_id")
    filter_addr = req.GET.get("addr")

    if(filter_id and filter_addr):
        influx_client = InfluxDBClient(
            filter_addr, "8086", "lab126", "lab126", "roda")
        cur_ts = int(time.time() * 10e8)

        query_cmd = "SELECT MEAN(EventMatchTime),MAX(EventMatchTime),Min(EventMatchTime) "\
            "FROM matchTime WHERE time > {} AND time < {}".format(
                cur_ts-1000000000, cur_ts)
        query_variance = "SELECT EventMatchTime FROM matchTime WHERE time > {} AND time < {}"\
            .format(cur_ts-1000000000, cur_ts)

        try:
            result = influx_client.query(query_cmd, epoch="ns")
            result_variance = influx_client.query(query_variance, epoch="ns")
            matchtime_result_list = list(result.get_points())
            varianceList = list(result_variance.get_points())
        except Exception as e:
            errmsg = "influx query failed: {}".format(e)
            roda.logger.error(
                errmsg+" {} + {}".format(query_cmd, query_variance))
            res["status"] = errmsg
            return HttpResponse(json.dumps(res), content_type="application/json")

        variance = 0.0
        for element in varianceList:
            diff = element['EventMatchTime'] - matchtime_result_list[0]['mean']
            variance = variance + diff * diff / len(varianceList)

        if(len(matchtime_result_list) == 0):
            res["data"] = {
                'average': 0,
                'maximum': 0,
                'minimum': 0,
                'variance': 0
            }
        else:
            first_ele = matchtime_result_list[0]
            res["data"] = {
                'average': first_ele['mean'],
                'maximum': first_ele['max'],
                'minimum': first_ele['min'],
                'variance': variance
            }
    else:
        res["status"] = "miss parameter"

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_GET
def filter_get_e2e_perf(req):
    res = {"status": "OK"}

    filter_addr = req.GET.get("addr")

    if(filter_addr):
        influx_client = InfluxDBClient(
            filter_addr, "8086", "lab126", "lab126", "roda")
        cur_ts = int(time.time() * 10e8)

        query_cmd = "SELECT MEAN(EventDelay),MAX(EventDelay),Min(EventDelay) "\
            "FROM clientTest WHERE time > {} AND time < {}".format(
                cur_ts-1000000000, cur_ts)
        query_variance = "SELECT EventDelay FROM clientTest WHERE time > {} AND time < {}"\
            .format(cur_ts-1000000000, cur_ts)

        try:
            result = influx_client.query(query_cmd, epoch="ns")
            result_variance = influx_client.query(query_variance, epoch="ns")
            matchtime_result_list = list(result.get_points())
            varianceList = list(result_variance.get_points())
        except Exception as e:
            errmsg = "influx query failed: {}".format(e)
            roda.logger.error(
                errmsg+" {} + {}".format(query_cmd, query_variance))
            res["status"] = errmsg
            return HttpResponse(json.dumps(res), content_type="application/json")

        variance = 0.0
        for element in varianceList:
            diff = element['EventDelay'] - matchtime_result_list[0]['mean']
            variance = variance + diff * diff

        if(len(matchtime_result_list) == 0):
            res["data"] = {
                'average': 0,
                'maximum': 0,
                'minimum': 0,
                'variance': 0
            }
        else:
            first_ele = matchtime_result_list[0]
            res["data"] = {
                'average': first_ele['mean'],
                'maximum': first_ele['max'],
                'minimum': first_ele['min'],
                'variance': variance / len(varianceList)
            }
    else:
        res["status"] = "miss parameter"

    return HttpResponse(json.dumps(res), content_type="application/json")
