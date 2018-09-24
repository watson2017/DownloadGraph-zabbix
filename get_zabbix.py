# - * - coding: utf-8 - * -

"""Zabbix-Api Get-Data CLI. 

Usage:[]
    get_zabbix.py download_graph --host=<kn> --graphname=<kn>
    get_zabbix.py get_max_network --host=<kn> --monitor_name=<kn>
    get_zabbix.py -h | --help
    get_zabbix.py --version

Options:
    download_graph           download specific picture from zabbix.
    get_max_network          get the max traffic of network.
    --host=<kn>              input remote host ip.
    -h, --help               display this help and exit.
    --version                output version information and exit.

Example：
    get_zabbix.py download_graph   --host="xxx"  --graphname="网卡流量 eth0"
    get_zabbix.py get_max_network  --host="xxx"  --monitor_name="net.if.out[eth0]"

"""

from docopt import docopt
from action import module


def action_route(doc_args):
    if doc_args.get("download_graph"): 
        module.get_graph(doc_args.get("--host"), doc_args.get("--graphname"))
    elif doc_args.get("get_max_network"):
        module.Get_max_network(doc_args.get("--host"), doc_args.get("--monitor_name"))
     
    else:
        print("An unreasonable parameters")



if  __name__ == '__main__':
    args = docopt(__doc__, version='Zabbix-Api-Get CLI 1.0')
    action_route(args)
