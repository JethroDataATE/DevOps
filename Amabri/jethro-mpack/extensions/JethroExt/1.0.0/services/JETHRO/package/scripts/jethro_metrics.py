import time
import httplib
import json
import sys
import socket
from resource_management.core.resources.system import File
from resource_management.libraries.functions.format import format
import os

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
        connection.request("POST", "/ws/v1/timeline/metrics", json_string, self.headers)

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


jethro_metrice_collector = JethroMetrics(sys.argv[1])
script_dir = os.path.dirname(os.path.abspath(__file__))
init_path = format('{script_dir}/../ams_host.ini')
File(init_path, content=sys.argv[1].split(':')[0])

while True:
    time.sleep(60)
    val = 0
    res = os.popen("service jethro status | awk '/JethroMaint/ {print $4}'")
    for service in res:
        val += 1
    jethro_metrice_collector.submit_metrics('jethro_maint', 'running_maint_services', val)
