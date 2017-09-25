import time
import httplib
import json
import socket


class JethroMetrics():

    metrics = []
    metrics_dict = dict()
    ams_collector_host = "ip-10-1-1-63.us-west-2.compute.internal"
    ams_collector_port = 6188
    headers = {"Content-type": "application/json"}
    my_hostname = "localhost"
    time_now =  0

    def __init__(self):
        self.time_now = int(time.time() * 1000.0)

    def submit_metrics(self):
        self.time_now = int(time.time() * 1000.0)
        self.my_hostname = socket.getfqdn()

        self.metrics.append(self.get_metrics("num_of_instances", self.get_num_of_instances()))
        self.metrics_dict["metrics"] = self.metrics
        json_string = json.JSONEncoder().encode(self.metrics_dict)

        connection = httplib.HTTPConnection(self.ams_collector_host, self.ams_collector_port, timeout=30)
        connection.request("POST", "ws/v1/timeline/metrics",json_string, self.headers)

    def get_num_of_instances(self):
        return 2

    def get_metrics(self, metric_name, metric_value):
        metric = {
            "metricname": metric_name,
            "appid": "jethro",
            "hostname": self.my_hostname,
            "timestamp": 0,
            "starttime": self.time_now,
            "metrics": {
                str(self.time_now): metric_value
            }
        }
        return metric
