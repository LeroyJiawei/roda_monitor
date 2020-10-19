from django.shortcuts import HttpResponse
import django.views.decorators.http as dj_http
import requests
import json
import traceback
import time
from docker import DockerClient as dockerClient
from io import BytesIO
from influxdb import InfluxDBClient

import monitor_backend.views_commons as roda


@dj_http.require_GET
def filter_list(req):
    res = {"status": "OK", "data": []}

    sql_list_filter = "SELECT `sink_sources`.`id`, `sink_sources`.`name`,"\
        "`sink_sources`.`source_data_system`, `sink_sources`.`source_info`,"\
        "`network`.`id` as `network_id`, `network`.`name` as `network_name`,"\
        "`network`.`vlan_addr` as `vlan_addr`, `sink_sources`.`docker_port`,"\
        "`sink_sources`.`state`,`network`.`addr` as `addr`,"\
        "`sink_sources`.`filter_base_rate`,"\
        "`sink_sources`.`filter_exp_match`,"\
        "`sink_sources`.`filter_win_size`,"\
        "`sink_sources`.`filter_max_thread`,"\
        "`sink_sources`.`filter_exist` "\
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
                "filter_base_rate": fil[10],
                "filter_exp_match": fil[11],
                "filter_win_size": fil[12],
                "filter_max_thread": fil[13],
                "filter_exist": "Yes" if fil[14] else "No",
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


@dj_http.require_POST
def filter_update_config(req):
    res = {"status": "OK"}

    post_param = json.loads(req.body.decode("UTF-8"))

    if("network_id" in post_param and
       "id" in post_param and
       "win_size" in post_param and
       "match_threshold" in post_param and
       "base_rate" in post_param and
       "max_thread" in post_param):

        sql_query = "SELECT `{}` FROM `network` WHERE `id`={}".format(
            'vlan_addr' if roda.Is_overlay_network else 'addr', post_param["network_id"])
        try:
            roda.mydb_cursor.execute(sql_query)
            result = roda.mydb_cursor.fetchone()
            influx_addr = result[0]
        except Exception as e:
            roda.logger.error(
                "get addr info [{}]:{}".format(sql_query, e))
            res["status"] = "get addr info: {}".format(e)
            return HttpResponse(json.dumps(res), content_type="application/json")

        try:
            influx_client = InfluxDBClient(
                influx_addr, 8086, "lab126", "lab126", "roda")

            influx_client.drop_measurement("dynamicParams")
            influx_client.write_points([{
                "measurement": "dynamicParams",
                "tags": {
                },
                "fields": {
                    "maxThreads": post_param["max_thread"],
                    "baseRate": post_param["base_rate"],
                    "matchWinSize": post_param["win_size"],
                    "expMatchTime": post_param["match_threshold"]
                }
            }])
        except Exception as e:
            roda.logger.error(
                "set dynamic param failed:{}".format(e))
            res["status"] = "set dynamic param failed:{}".format(e)
            return HttpResponse(json.dumps(res), content_type="application/json")

        sql_query = "UPDATE `sink_sources` SET "\
            "`filter_base_rate`={}, `filter_exp_match`={},"\
            "`filter_win_size`={}, `filter_max_thread`={},"\
            "`filter_exist`=TRUE WHERE `id`={}".format(
                post_param["base_rate"], post_param["match_threshold"],
                post_param["win_size"], post_param["max_thread"], post_param["id"])
        try:
            roda.mydb_cursor.execute(sql_query)
            roda.mydb_client.commit()

        except Exception as e:
            roda.mydb_client.rollback()
            roda.logger.error(
                "update info falied [{}]:{}".format(sql_query, e))
            res["status"] = "update info falied : {}".format(e)
            return HttpResponse(json.dumps(res), content_type="application/json")

    else:
        res["status"] = "miss parameter"

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_http_methods(["DELETE"])
def filter_delete(req):
    res = {"status": "OK"}

    delete_param = json.loads(req.body.decode("UTF-8"))

    if("id" in delete_param):
        sql_query = "SELECT `network`.`{}` as `addr`, "\
            "`sink_sources`.`filter_exist`,`sink_sources`.`docker_port` "\
            "FROM `sink_sources` "\
            "JOIN `network` ON `sink_sources`.`network_id`=`network`.`id` "\
            "WHERE `sink_sources`.`id`={}".format(
                'vlan_addr' if roda.Is_overlay_network else 'addr',
                delete_param["id"])
        try:
            roda.mydb_cursor.execute(sql_query)
            result = roda.mydb_cursor.fetchone()
            docker_addr = result[0]
            filter_exist = result[1]
            docker_port = result[2]
            if(not filter_exist):
                res["status"] = "filter container does not exist"
                return HttpResponse(json.dumps(res), content_type="application/json")

        except Exception as e:
            roda.logger.error(
                "get filter info [{}]:{}".format(sql_query, e))
            res["status"] = "get addr info: {}".format(e)
            return HttpResponse(json.dumps(res), content_type="application/json")

        try:
            docker_client = dockerClient(
                base_url="tcp://{}:{}".format(docker_addr, docker_port))
            container_info = docker_client.containers.get(
                container_id="filter")
            container_info.stop()
            container_info.remove()
        except Exception as e:
            errmsg = "stop filter failed: {}".format(e)
            res["status"] = errmsg
            roda.logger.error(errmsg)
            return HttpResponse(json.dumps(res), content_type="application/json")

        try:
            sql_query = "UPDATE `sink_sources` SET "\
                "`filter_base_rate`=null, `filter_exp_match`=null,"\
                "`filter_win_size`= null, `filter_max_thread`=null,"\
                "`filter_exist`=FALSE WHERE `id`={}".format(delete_param['id'])
            roda.mydb_cursor.execute(sql_query)
            roda.mydb_client.commit()
        except Exception as e:
            roda.mydb_client.rollback()
            res["status"] = "update removed info failed: {}".format(e)

    else:
        res["status"] = "miss parameter"

    return HttpResponse(json.dumps(res), content_type="application/json")
