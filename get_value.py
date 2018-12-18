# - * - coding: utf-8-sig - * -

import configparser
def get_message(value):
    cf = configparser.ConfigParser()
    cf.read(r'E:\work\zabbix-graph\get-zabbix\conf\config.ini',encoding="utf-8-sig")
    return cf.get("info",value)
