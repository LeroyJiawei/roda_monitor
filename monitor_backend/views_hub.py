from django.shortcuts import HttpResponse
import django.views.decorators.http as dj_http
import requests
import json
import traceback
from docker import DockerClient as dockerClient
from docker import APIClient
from io import BytesIO
from influxdb import InfluxDBClient
from roda_monitor.settings import BASE_DIR
import os

import monitor_backend.views_commons as roda


@dj_http.require_GET
def hub_info(req):
    res = {"status": "OK", "data": {}}

    sql_get_hub_addr = "SELECT `{}`,`service_port`,`docker_port` "\
        "FROM `network` WHERE `role` = 'hub-edge'".format(
            "vlan_addr" if roda.Is_overlay_network else "addr")
    try:
        roda.mydb_cursor.execute(sql_get_hub_addr)
        hub_addr = roda.mydb_cursor.fetchone()
    except Exception as e:
        roda.logger.error("Get Hub (vlan) addr query [{}] failed: [{}]".format(
            sql_get_hub_addr, e))
        roda.logging.exception(e)
        res["status"] = "Get Hub (vlan) addr query failed: [{}]".format(e)

    res["data"] = {
        "vlan_addr" if roda.Is_overlay_network else "addr": hub_addr[0],
        "port": hub_addr[1],
        "docker_port": hub_addr[2]
    }

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_GET
def hub_list_images(req):
    res = {"status": "OK", "data": []}

    sql_get_hub_addr = "SELECT `{}`,`service_port` FROM `network` WHERE "\
        " `role` = 'hub-edge'".format(
            "vlan_addr" if roda.Is_overlay_network else "addr")
    try:
        roda.mydb_cursor.execute(sql_get_hub_addr)
        if(roda.mydb_cursor.description):
            hub_addr = roda.mydb_cursor.fetchone()
    except Exception as e:
        roda.logger.error("Get Hub (vlan) addr query [{}] failed: [{}]".format(
            sql_get_hub_addr, e))
        roda.logging.exception(e)
        res["status"] = "Get Hub (vlan) addr query failed: [{}]".format(e)
        return HttpResponse(json.dumps(res), content_type="application/json")

    try:
        hub_resp = requests.get(
            "http://{}:{}/v2/_catalog".format(hub_addr[0], hub_addr[1]))
        roda.logging.info("http://{}:{}/v2/_catalog".format(
            hub_addr[0], hub_addr[1]))
        repo_list = hub_resp.json()["repositories"]

        for repo in repo_list:
            hub_resp = requests.get(
                "http://{}:{}/v2/{}/tags/list".format(hub_addr[0], hub_addr[1], repo))
            tag_list = hub_resp.json()

            if tag_list["tags"] and len(tag_list["tags"]) > 0:
                for tag in tag_list["tags"]:
                    res["data"].append({
                        "name": "{}:{}/{}".format(hub_addr[0], hub_addr[1], tag_list["name"]),
                        "tag": tag
                    })
    except Exception as e:
        errmsg = "Get Hub repository tags failed: {}".format(e)
        roda.logger.error(errmsg)
        res["status"] = errmsg

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_http_methods(["DELETE"])
def hub_delete_image(req):
    res = {"status": "OK"}

    delete_data = json.loads(req.body.decode("UTF-8"))

    if('name' in delete_data and 'tag' in delete_data and
       "hub_addr" in delete_data and "hub_port" in delete_data):
        try:
            image_name = delete_data["name"].split('/')[-1]
            image_tag = delete_data["tag"]
            hub_addr = delete_data["hub_addr"]
            hub_port = delete_data["hub_port"]

            roda.logger.info("query {}".format("http://{}:{}/v2/{}/manifests/{}".format(
                hub_addr, hub_port, image_name, image_tag)))
            hub_resp = requests.get(
                "http://{}:{}/v2/{}/manifests/{}".format(
                    hub_addr, hub_port, image_name, image_tag),
                headers={"Accept": "application/vnd.docker.distribution.manifest.v2+json"})
            image_digest = hub_resp.headers["Docker-Content-Digest"]

            roda.logger.info("image_digest of {}:{} is ".format(
                image_name, image_tag)+image_digest)

            hub_resp = requests.delete(
                "http://{}:{}/v2/{}/manifests/{}".format(
                    hub_addr, hub_port, image_name, image_digest))

            if(hub_resp.status_code != 202):
                raise ValueError("Status Code of delete is not 202")

        except Exception as e:
            errmsg = "Delete Hub repository tags failed: {}".format(e)
            roda.logger.error(errmsg)
            res["status"] = errmsg
    else:
        res["status"] = "miss parameter"

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_GET
def hub_list_docker_images(req):

    docker_port = req.GET.get("docker_port")

    res = {"status": "OK"}

    if(docker_port):

        sql_get_hub_addr = "SELECT `{}` FROM `network` WHERE"
        " `role` = 'hub-edge'".format(
            "vlan_addr" if roda.Is_overlay_network else "addr")
        try:
            roda.mydb_cursor.execute(sql_get_hub_addr)
            hub_addr = roda.mydb_cursor.fetchone()
        except Exception as e:
            roda.logger.error("Get Hub (vlan) addr query [{}] failed: [{}]".format(
                sql_get_hub_addr, e))
            res["status"] = "Get Hub (vlan) addr query failed: [{}]".format(e)
            return HttpResponse(json.dumps(res), content_type="application/json")

        try:
            docker_cli = dockerClient(
                base_url='tcp://{}:{}'.format(hub_addr[0], docker_port))
            res["data"] = docker_cli.images()
        except Exception as e:
            errmsg = "Get Hub docker engine images failed: [{}]".format(e)
            roda.logger.error(errmsg)
            res["status"] = errmsg
    else:
        res["status"] = "miss parameter"

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_POST
def hub_run_image(req):
    res = {"status": "OK"}

    post_data = json.loads(req.body.decode("UTF-8"))

    if("target_id" in post_data and
        "image_name" in post_data and
        "image_tag" in post_data and
        "source_info" in post_data and
        "sink_info" in post_data and
        "max_attr" in post_data and
        "win_size" in post_data and
        "match_threshold" in post_data and
        "max_thread" in post_data and
            "base_rate" in post_data):

        target_id = post_data["target_id"]
        image_name = post_data["image_name"]
        image_tag = post_data["image_tag"]
        source_info = post_data["source_info"]
        sink_info = post_data["sink_info"]
        max_attr = post_data["max_attr"]
        win_size = post_data["win_size"]
        match_threshold = post_data["match_threshold"]
        max_thread = post_data["max_thread"]
        base_rate = post_data["base_rate"]

        sql_query = "SELECT `network`.`{}` as `addr`, "\
                    "`network`.`docker_port` as `port`, "\
                    "`sink_sources`.`ap_lan_addr` as `ap_lan_addr`, "\
                    "`sink_sources`.`filter_exist` as `filter_exist`, "\
                    "`sink_sources`.`influx_port` as `influx_port`,"\
                    "`sink_sources`.`domain_map` as `domain_map` "\
                    "FROM `sink_sources` "\
                    "JOIN `network` ON `sink_sources`.`network_id`=`network`.`id` "\
                    "WHERE `sink_sources`.`id`={}".format(
                        'vlan_addr' if roda.Is_overlay_network else 'addr', target_id)

        try:
            roda.mydb_cursor.execute(sql_query)
            result = roda.mydb_cursor.fetchone()
            docker_addr = result[0]
            docker_port = result[1]
            ap_lan_addr = result[2]
            filter_exist = result[3]
            influx_port = result[4]
            domain_map = result[5]

            domain_lists = {}

            for d_ip in domain_map.split(','):
                d_ip_split = d_ip.split(':')
                domain_lists[d_ip_split[0]] = d_ip_split[1]

            if(filter_exist):
                res["status"] = "Filter exist in the source system"
                return HttpResponse(json.dumps(res), content_type="application/json")

            docker_client = dockerClient(
                base_url="tcp://{}:{}".format(docker_addr, docker_port))

            container_info = docker_client.containers.run(
                image="{}:{}".format(image_name, image_tag),
                detach=True,
                name="filter",
                environment={
                    "SINK": "{}".format(sink_info),
                    "SOURCE": "{}".format(source_info),
                    "MAXATTR": max_attr,
                    "INFLUX": "http://{}:8086".format(ap_lan_addr)
                },
                extra_hosts=domain_lists
            )

            roda.logger.info(
                "run image success [{}:{}]".format(image_name, image_tag))

        except Exception as e:
            roda.logger.error("run image failed [{}]:{}".format(sql_query, e))
            res["status"] = "run image failed: {}".format(e)
            return HttpResponse(json.dumps(res), content_type="application/json")

        try:
            influx_client = InfluxDBClient(
                docker_addr, influx_port, "lab126", "lab126", "roda")
            influx_client.drop_measurement("dynamicParams")
            influx_client.write_points([{
                "measurement": "dynamicParams",
                "tags": {
                },
                "fields": {
                    "maxThreads": int(max_thread),
                    "baseRate": base_rate,
                    "matchWinSize": int(win_size),
                    "expMatchTime": int(match_threshold)
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
                    base_rate, match_threshold,
                    win_size, max_thread, target_id)
        try:
            roda.mydb_cursor.execute(sql_query)
            roda.mydb_client.commit()
        except Exception as e:
            roda.mydb_client.rollback()
            roda.logger.error(
                "update info failed [{}]:{}".format(sql_query, e))
            res["status"] = "update mysql info failed: {}".format(e)

    else:
        res["status"] = "miss parameter"
        return HttpResponse(json.dumps(res), content_type="application/json")

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_POST
def hub_upload_file(req):
    res = {"status": "OK"}

    obj = req.FILES.get('file', None)

    if not obj:
        res["status"] = "miss parameter file"
        resp = HttpResponse(json.dumps(res), content_type="application/json")
        resp.status_code = 415
        return resp

    if obj.name[-1] == "\"":
        obj.name = obj.name[:-1]

    new_file_path = os.path.join(BASE_DIR, 'image_build_files',
                                 'tarFiles', obj.name)
    if os.path.exists(new_file_path):
        res["status"] = "file exits"
        resp = HttpResponse(json.dumps(res), content_type="application/json")
        resp.status_code = 415
        return resp

    f = open(new_file_path, 'wb')
    for chunk in obj.chunks():
        f.write(chunk)
    f.close()

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_GET
def hub_list_file(req):
    res = {"status": "OK"}

    tar_file_path = os.path.join(BASE_DIR, 'image_build_files',
                                 'tarFiles')
    file_list = os.listdir(tar_file_path)

    res["data"] = []
    for f in file_list:
        res["data"].append({"name": f,
                            "url": "http://{}/static/{}".format(
                                roda.DomainName, f)})

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_http_methods(["DELETE"])
def hub_delete_file(req):
    res = {"status": "OK"}

    post_data = json.loads(req.body.decode("UTF-8"))

    if("file_name" in post_data):
        delete_file_path = os.path.join(BASE_DIR, 'image_build_files',
                                        'tarFiles', post_data["file_name"])

        if os.path.exists(delete_file_path):
            os.remove(delete_file_path)

    else:
        res["status"] = "miss parameter"

    return HttpResponse(json.dumps(res), content_type="application/json")


@dj_http.require_POST
def hub_upload_dockerfile(req):
    res = {"status": "OK"}

    file_obj = req.FILES.get('file', None)
    hub_addr = req.POST.get('addr', None)
    hub_port = req.POST.get('port', None)
    docker_port = req.POST.get('docker_port', None)
    new_image_name = req.POST.get('new_image_name', None)
    new_image_tag = req.POST.get('new_image_tag', "latest")

    if(file_obj and hub_addr and hub_port and
       new_image_name and docker_port):
        try:
            docker_cli = APIClient(
                base_url="tcp://{}:{}".format(hub_addr, docker_port))
            docker_resp = docker_cli.build(
                fileobj=BytesIO(file_obj.read()), rm=True, tag="{}:{}/{}:{}".format(
                    hub_addr, hub_port, new_image_name, new_image_tag))
            for line in docker_resp:
                line_stream_info = line.decode("UTF-8")
                if("stream" not in line_stream_info and
                   "aux" not in line_stream_info):
                    errmsg = "Build new image '{}:{}' failed: {}".format(
                        new_image_name, new_image_tag,
                        line_stream_info)
                    roda.logger.error(errmsg)
                    res["status"] = errmsg
                    resp = HttpResponse(json.dumps(
                        res), content_type="application/json")
                    resp.status_code = 415
                    return resp
                    break
                else:
                    roda.logger.info(line_stream_info)

            roda.logger.info("Build new image '{}:{}' success".format(
                new_image_name, new_image_tag))

        except Exception as e:
            errmsg = "Build new image '{}:{}' failed: {}".format(
                new_image_name, new_image_tag, e)
            roda.logger.error(errmsg)
            traceback.print_exc()
            res["status"] = errmsg
            resp = HttpResponse(json.dumps(
                res), content_type="application/json")
            resp.status_code = 415
            return resp

        try:
            docker_resp = docker_cli.push(
                "{}:{}/{}".format(hub_addr, hub_port, new_image_name),
                tag=new_image_tag, stream=True, decode=True)
            for line in docker_resp:
                roda.logger.info(line)
            roda.logger.info("Push new image '{}:{}' to {}:{} success".format(
                new_image_name, new_image_tag, hub_addr, hub_port))
        except Exception as e:
            for line in docker_resp:
                roda.logger.error(line)
            errmsg = "Push new image '{}:{}' failed: {}".format(
                new_image_name, new_image_tag, e)
            roda.logger.error(errmsg)
            traceback.print_exc()
            res["status"] = errmsg
            resp = HttpResponse(json.dumps(
                res), content_type="application/json")
            resp.status_code = 415

    else:
        res["status"] = "miss parameter"
        resp = HttpResponse(json.dumps(res), content_type="application/json")
        resp.status_code = 415
        return resp

    return HttpResponse(json.dumps(res), content_type="application/json")
