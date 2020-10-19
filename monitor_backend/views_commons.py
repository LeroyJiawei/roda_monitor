from configparser import ConfigParser
import mysql.connector
import logging
import traceback


logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s - %(filename)s:%(funcName)s:%(lineno)s"
                    " - %(levelname)s] %(message)s")
logger = logging.getLogger("Roda_monito_views")

Is_overlay_network = False
DomainName = "None"

try:
    cfg = ConfigParser()
    cfg.read('config.ini')
    mysql_host = cfg.get('mysql', 'host')
    mysql_port = cfg.get('mysql', 'port')
    mysql_user = cfg.get('mysql', 'username')
    mysql_passwd = cfg.get('mysql', 'passwd')
    mysql_db = cfg.get('mysql', 'database')
    DomainName = cfg.get('roda', 'domain')

    mydb_client = mysql.connector.connect(
        host=mysql_host,
        port=mysql_port,
        user=mysql_user,
        passwd=mysql_passwd,
        database=mysql_db,
        buffered=True
    )

    sql_query = "SELECT `value` FROM `universe` WHERE `config_name`='is_overlay' "

    mydb_cursor = mydb_client.cursor()
    mydb_cursor.execute(sql_query)
    resp = mydb_cursor.fetchall()
    if(len(resp) >= 1 and len(resp[0]) >= 1):
        Is_overlay_network = True if resp[0][0] != 0 else False
    else:
        raise ValueError(
            "cannot get the information wether roda is use overlay network")

except Exception as e:
    logger.error(
        "init failed to parse configuration file or database connect: {}".format(e))
    traceback.print_exc()
    exit(1)


# :param key -- json key
# :param http_param -- json form data from http request
# :param is_int -- is current type int form
def current_val_or_null(key, http_param, is_int):
    cond = key in http_param and (http_param[key] not in ["", None, "null"])
    if is_int:
        return "{}".format(http_param[key]) if cond else 'null'
    else:
        return "'{}'".format(http_param[key]) if cond else 'null'
