from configparser import ConfigParser
import mysql.connector
from influxdb import InfluxDBClient
import logging
import traceback


logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s - %(name)s] - %(levelname)s - %(message)s')
logger = logging.getLogger("Roda_monito_views")

try:
    cfg = ConfigParser()
    cfg.read('config.ini')
    mysql_host = cfg.get('mysql', 'host')
    mysql_port = cfg.get('mysql', 'port')
    mysql_user = cfg.get('mysql', 'username')
    mysql_passwd = cfg.get('mysql', 'passwd')
    mysql_db = cfg.get('mysql', 'database')

    influx_host = cfg.get('influxdb', 'host')
    influx_port = cfg.get('influxdb', 'port')
    influx_user = cfg.get('influxdb', 'username')
    influx_passwd = cfg.get('influxdb', 'passwd')
    influx_db = cfg.get('influxdb', 'database')

    mydb_client = mysql.connector.connect(
        host=mysql_host,
        port=mysql_port,
        user=mysql_user,
        passwd=mysql_passwd,
        database=mysql_db
    )
    mydb_cursor = mydb_client.cursor()

    influx_client = InfluxDBClient(influx_host, influx_port,
                                   influx_user, influx_passwd, influx_db)
except Exception as e:
    logger.info(
        "init failed to parse configuration file or database connect: {}".format(e))
    traceback.print_exc()
