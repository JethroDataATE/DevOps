import time
import httplib
import json
import sys
import socket
from resource_management.core.resources.system import File
from resource_management.libraries.functions.format import format
import os
from jethro_metrics_utils import read_metric_values, instance_name_to_number


class JethroMetrics():

    metrics = []
    metrics_dict = dict()
    ams_collector_address = "0.0.0.0:6188"
    headers = {"Content-type": "application/json"}
    my_hostname = "localhost"
    time_now = 0

    def __init__(self, ams_collector_address):
        self.time_now = int(time.time() * 1000.0)
        self.ams_collector_address = ams_collector_address

    def submit_metrics(self, appid, metric_name, metric_value):
        self.time_now = int(time.time() * 1000.0)
        self.my_hostname = socket.getfqdn()

        self.metrics.append(self.get_metrics(appid, metric_name, metric_value))
        self.metrics_dict["metrics"] = self.metrics
        json_string = json.JSONEncoder().encode(self.metrics_dict)

        connection = httplib.HTTPConnection(self.ams_collector_address)
        connection.request("POST", "/ws/v1/timeline/metrics",
                           json_string, self.headers)

        try:
            response = connection.getresponse()
            print(response.status, response.reason)
            print(response.read())
            if response.status == 200:
                print("Successful sending Jethro metric to Ambari Metric Collector.")
            else:
                print("Error sending Jethro metric to Ambari Metric Collector.")
        except Exception as e:
            print("Unable to get a response from Ambari Metric Collector: " + str(e))
        connection.close()

    def get_metrics(self, appid, metric_name, metric_value):
        metric = {
            "metricname": metric_name,
            "appid": appid,
            "hostname": self.my_hostname,
            "timestamp": self.time_now,
            "starttime": self.time_now,
            "metrics": {
                str(self.time_now): metric_value
            }
        }
        return metric

#**************** Main Logic *************************

ams_address = sys.argv[1]
jethro_metrice_collector = JethroMetrics(ams_address)
script_dir = os.path.dirname(os.path.abspath(__file__))
init_path = format('{script_dir}/../ams_host.ini')
ams_host = ams_address.split(':')[0]
ams_port = int(ams_address.split(':')[1])
os.popen('echo ' + ams_host + ' > ' + init_path)


def submit_attached_instances_names_metrics():
    res = os.popen("awk -F \":\" '$1 !~ /#/ {x=$1} {if (x != \"\") print x}' /opt/jethro/instances/services.ini")
    for instance_name in res:
        instance_num = instance_name_to_number(instance_name)
        jethro_metrice_collector.submit_metrics('jethro_mng', 'attached_instances_names', instance_num)


def format_instance_name(instance_name):
    return instance_name[9:-7]

def submit_running_instances_names_metrics():
    res = os.popen("service jethro status | awk '{print $2}'")
    instances = []

    for instance in res:
        instance_name = format_instance_name(instance)
        instance_num = instance_name_to_number(instance_name)
        if instance_num not in instances:
            instances.append(instance_num)

    for instance_num in instances:
        jethro_metrice_collector.submit_metrics('jethro_mng', 'running_instances_names', instance_num)

def submit_running_instances_metrics():

    metrics = read_metric_values(ams_host, ams_port, False, "jethro_mng", "running_instances_names")

    val = len(set(metrics))

    jethro_metrice_collector.submit_metrics('jethro_mng', 'running_instances', val)

def submit_maint_status_metrics():
    res = os.popen("service jethro status | awk '/JethroMaint/ {print $2}'")
    for instance in res:
        instance_name = format_instance_name(instance)
        instance_num = instance_name_to_number(instance_name)
        jethro_metrice_collector.submit_metrics('jethro_maint', 'running_maint_services', instance_num)


def submit_load_scheduler_status_metrics():
    res = os.popen("service jethro status | awk '/JethroLoadsScheduler/ {print $2}'")
    for instance in res:
        instance_name = format_instance_name(instance)
        instance_num = instance_name_to_number(instance_name)
        jethro_metrice_collector.submit_metrics('jethro_load_scheduler', 'running_load_scheduler_services', instance_num)


while True:
    time.sleep(60)

    try:
        submit_attached_instances_names_metrics()
        submit_maint_status_metrics()
        submit_load_scheduler_status_metrics()
        submit_running_instances_names_metrics()
        submit_running_instances_metrics()
    except Exception as e:
        print("Unable to submit Jethro metrics to Ambari Metric Collector: " + str(e))
