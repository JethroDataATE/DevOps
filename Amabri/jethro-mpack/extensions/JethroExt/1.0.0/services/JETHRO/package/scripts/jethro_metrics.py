import time
import httplib
import json
import sys
import socket
from resource_management.core.resources.system import File
from resource_management.libraries.functions.format import format

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

    def submit_metrics(self):
        self.time_now = int(time.time() * 1000.0)
        self.my_hostname = socket.getfqdn()

        self.metrics.append(self.get_metrics("running_instances", self.get_num_of_instances()))
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
        except:
            print("Unable to get a response from Ambari Metric Collector.")
        connection.close()

    def get_num_of_instances(self):
        running_instances = []
        connection = httplib.HTTPConnection("localhost", 9100, timeout=30)
        connection.request("GET", "/api/Nodes/getServices")
        try:
            response = connection.getresponse()

            if response.status == 200:
                res = response.read()
                print(res)
                json_data = json.loads(res)
                print (json_data)
                instances = json_data["services"]
                print(instances)
                running_instances = [a for a in instances if a['status'] == 'running']
            else:
                print("Error getting Jethro instances information.")
        except:
            e = sys.exc_info()[0]
            print("Unable to get Jethro instances information.", e)
        connection.close()
        return len(running_instances)

    def get_metrics(self, metric_name, metric_value):
        metric = {
            "metricname": metric_name,
            "appid": "jethro_mng",
            "hostname": self.my_hostname,
            "timestamp": self.time_now,
            "starttime": self.time_now,
            "metrics": {
                str(self.time_now): metric_value
            }
        }
        return metric


jethro_metrice_collector = JethroMetrics(sys.argv[1])
while True:
    time.sleep(30)
    jethro_metrice_collector.submit_metrics()

