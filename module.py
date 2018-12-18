# - * - coding: utf-8-sig - * -
import json
import requests
import urllib
import datetime,time
import http.cookiejar
import  xlsxwriter
import os
from conf import get_value


urls = 'http://xxx/zabbix/api_jsonrpc.php'
user = get_value.get_message("user")
password = get_value.get_message("password")
gr_url = "http://xxx/zabbix/chart2.php"
login_url = 'http://xxx/zabbix/index.php'
endtime = time.time()
starttime = int(time.mktime((datetime.datetime.now() - datetime.timedelta(days = 7)).timetuple())) 
dirs = r"E:\work\xxx\%s"  %(datetime.datetime.now().strftime('%Y%m%d'))

parms = {
   "jsonrpc": "2.0",
   "method": "user.login",
   "params": {
       "user": user,
       "password": password
       },
   "id": 1
}

headers = {
   'Content-Type': 'application/json'
}

login_data = urllib.parse.urlencode({
                       "name": user,
                       "password": password,
                       "autologin": 1,
                       "enter": "Sign in"}).encode(encoding='UTF8')


# 获取token
def get_token():
   req = requests.get(urls, headers=headers, data=json.dumps(parms))
   key = req.text
   dic = json.loads(key)
   token = dic['result']
   return token


# 获取主机的id
def get_hostid(hostnameid):
   hostid_parms = {
       "jsonrpc": "2.0",
       "method": "host.get",
       "params": {
           "output": "extend",
           "filter": {
               "host": [
                   hostnameid
               ]
           }
       },
       "auth": get_token(),
       "id": 1
   }
   hostid = requests.get(urls, headers=headers, data=json.dumps(hostid_parms))
   result = json.loads(hostid.text)['result'][0]['hostid']
   return result


def getgraphid(hostname,graphname):
   '''定义通过hostid获取graphid的函数'''
   values = {
       "jsonrpc": "2.0",
       "method": "graph.get",
       "params": {
           "output": "name",
           "hostids": get_hostid(hostname),
           "sortfield": "name",
           "filter": {
               "name": graphname
           }
       },
       "auth": get_token(),
       "id": 10
   }
   req = requests.get(urls, headers=headers, data=json.dumps(values)).text
   result = json.loads(req)['result'][0]['graphid']
   return result                


def get_graph(hostname,graphname):
   '''download graph from zabbix api'''

   graph_args = urllib.parse.urlencode({
                       "graphid": getgraphid(hostname,graphname),
                       "width":'1200',
                       "height":'156',
                       "stime":starttime, #图形开始时间
                       "period":'604800'}).encode(encoding='UTF8')

   cj = http.cookiejar.CookieJar()   # 设置一个cookie处理器, 它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
   opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
   urllib.request.install_opener(opener)
   opener.open(login_url, login_data).read()
   data = opener.open(gr_url, graph_args).read()
   
   if os.path.exists(dirs):
       pass
   else:
       os.makedirs(dirs)
   with open(r"%s\%s.png" % (dirs, hostname), 'wb') as f:
       f.write(data)


def items_get(hostname, monitor_name):

   items_get_network = {
       "jsonrpc": "2.0",
       "method": "item.get",
       "params":{
           "output":"itemids",
           "hostids": get_hostid(hostname),
           "search":{
           'key_': monitor_name
           },
       },
       "auth":get_token(),
       "id":0
   }
   req = requests.get(urls, headers=headers, data=json.dumps(items_get_network)).text
   result = json.loads(req)['result'][0]['itemid']
   return result


def Get_max_network(hostname, monitor_name):
   '''获取一周内最大的监控值'''
   test = {
       "jsonrpc": "2.0",
       "method": "history.get",
       "params": {
           "output": "extend",
           "history": 3,
           "itemids": items_get(hostname, monitor_name),
           "sortfield": "clock",
           "sortorder": "DESC",
           "time_from": starttime,
           "time_till": endtime
       },
       "auth": get_token(),
       "id": 0
   }

   req = requests.get(urls, headers=headers, data=json.dumps(test)).text
   result = json.loads(req)['result']
   li = []
   for i in result:
       li.append(int(i['value'])) 
   li.sort()
   return str(round(li[-1]/1000/1000,2))+" Mbps"


# get_token()
