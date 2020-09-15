from django.shortcuts import render, HttpResponse
from configparser import ConfigParser
import django.views.decorators.http as dj_http
from influxdb import InfluxDBClient
import logging
import json
import datetime
import requests
import time

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s - %(name)s] - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

cfg = ConfigParser()
cfg.read('config.ini')
influx_host = cfg.get('influxdb', 'host')
influx_port = cfg.get('influxdb', 'port')
influx_user = cfg.get('influxdb', 'username')
influx_passwd = cfg.get('influxdb', 'passwd')
influx_db = cfg.get('influxdb', 'database')

client = InfluxDBClient(influx_host, influx_port,
                        influx_user, influx_passwd, influx_db)
i_count = 0
match_timestamp = 1599471156644732552
j_count = 0
sub_match_timestamp = 1599471156644732552

# Create your views here.


def index_fun(request):
    return render(request, "index.html")


@dj_http.require_GET
def getMatchTime(request):
    matchtime_result_list = []
    global i_count
    global match_timestamp
    query_cmd = "SELECT MEAN(EventMatchTime),MAX(EventMatchTime),Min(EventMatchTime)  "\
        "FROM \"matchTime\" where time > {} and time < {}".format(
            match_timestamp, match_timestamp+1000000000)

    query_variance = "SELECT EventMatchTime FROM \"matchTime\" where time > {} and time < {}"\
        .format(match_timestamp, match_timestamp+1000000000)
    result = client.query(query_cmd, epoch="ns")
    result_variance = client.query(query_variance, epoch="ns")
    matchtime_result_list = list(result.get_points())
    varianceList = list(result_variance.get_points())
    # print(varianceList)
    # print(matchtime_result_list)
    variance = 0
    for element in varianceList:
        variance = variance + (element['EventMatchTime']-matchtime_result_list[0]['mean'])*(
            element['EventMatchTime']-matchtime_result_list[0]['mean'])/len(varianceList)

    # print(variance)
    i_count += 1
    if(len(matchtime_result_list) == 0):
        match_timestamp = match_timestamp + 1000000000
        res = json.dumps({
            'time': i_count,
            'average': 0,
            'maximum': 0,
            'minimum': 0,
            'variance': 0
        })
    else:
        first_ele = matchtime_result_list[0]
        match_timestamp = match_timestamp + 1000000000
        first_ele['time'] = i_count
        res = json.dumps({
            'time': i_count,
            'average': first_ele['mean'],
            'maximum': first_ele['max'],
            'minimum': first_ele['min'],
            'variance': variance
        })

    return HttpResponse(res)


@dj_http.require_GET
def getSubMatchTime(request):
    logger.info("Get into getSubMatchTime")
    matchtime_result_list = []
    global i_count
    global sub_match_timestamp
    query_cmd = "SELECT MEAN(EventDelay),MAX(EventDelay),Min(EventDelay)  "\
        "FROM \"client-test\" where time > {} and time < {}"\
        .format(sub_match_timestamp, sub_match_timestamp+1000000000)
    query_variance = "SELECT EventDelay FROM \"matchTime\" "\
        "where time > {} and time < {}"\
        .format(sub_match_timestamp, sub_match_timestamp+1000000000)
    result = client.query(query_cmd, epoch="ns")
    result_variance = client.query(query_variance, epoch="ns")
    matchtime_result_list = list(result.get_points())
    varianceList = list(result_variance.get_points())
    variance = 0
    for element in varianceList:
        variance = variance + (element['EventDelay']-matchtime_result_list[0]['mean'])*(
            element['EventDelay']-matchtime_result_list[0]['mean'])/len(varianceList)

    i_count += 1
    if(len(matchtime_result_list) == 0):
        sub_match_timestamp = sub_match_timestamp + 1000000000
        res = json.dumps({
            'time': i_count,
            'average': 0,
            'maximum': 0,
            'minimum': 0,
            'variance': 0
        })
    else:
        first_ele = matchtime_result_list[0]
        sub_match_timestamp = sub_match_timestamp + 1000000000
        first_ele['time'] = i_count
        res = json.dumps({
            'time': i_count,
            'average': first_ele['mean'],
            'maximum': first_ele['max'],
            'minimum': first_ele['min'],
            'variance': variance
        })

    return HttpResponse(res)
