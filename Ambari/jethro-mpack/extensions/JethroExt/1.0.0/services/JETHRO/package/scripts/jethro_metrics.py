import time
import httplib
import json
import sys
import socket
from resource_management.libraries.functions.format import format
import os
from jethro_metrics_utils import read_metric_values, instance_name_to_number


class JethroMetrics():

    # metrics = []
    metrics_dict = dict()
    ams_collector_address = "0.0.0.0:6188"
    headers = {"Content-type": "application/json"}
    my_hostname = "localhost"
    time_now = 0

    def __init__(self, ams_collector_address):
        self.time_now = int(time.time() * 1000.0)
        self.ams_collector_address = ams_collector_address

    def submit_metrics(self, appid, metric_name, metric_values):
        
        self.metrics = []

        self.time_now = int(time.time() * 1000.0)
        self.my_hostname = socket.getfqdn()

        self.metrics.append(self.get_metrics(appid, metric_name, metric_values))
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

    def get_metrics(self, appid, metric_name, metric_values):
        vals = {}
        i = 0
        for val in metric_values:
            vals[str(self.time_now + (i * 1000))] = val
            i = i +1

        metric = {
            "metricname": metric_name,
            "appid": appid,
            "hostname": self.my_hostname,
            "timestamp": self.time_now,
            "starttime": self.time_now,
            "metrics": vals
        }
        return metric

#****************  Helpers *************************


def submit_attached_instances_names_metrics():
    res = os.popen("awk -F \":\" '$1 !~ /#/ {x=$1} {if (x != \"\") print x}' /opt/jethro/instances/services.ini")
    instances = []
    for instance_name in res:
        instance_num = instance_name_to_number(instance_name.replace('LF', ''))
        instances.append(instance_num)
    jethro_metrice_collector.submit_metrics('jethro_mng', 'attached_instances_names', instances)


def format_instance_name(instance_name):
    return instance_name[9:-7]


def submit_running_instances_names_metrics(jethro_version):
    
    jethro_status_cmd = "service jethro status | awk '{if($2 != \"JethroMonitor\") print $5}'"

    # service status prompt has change from version 3.4.2
    if(jethro_version < "3.4.2"):
        jethro_status_cmd = "service jethro status | awk '{print $2}'"

    res = os.popen(jethro_status_cmd)

    instances = []
    for instance in res:
        instance_name = format_instance_name(instance)
        instance_num = instance_name_to_number(instance_name)
        if instance_num not in instances:
            instances.append(instance_num)

    jethro_metrice_collector.submit_metrics('jethro_mng', 'running_instances_names', instances)


def submit_running_instances_metrics():

    metrics = read_metric_values(ams_host, ams_port, False, "jethro_mng", "running_instances_names", 3)

    val = len(set(metrics))
    vals = []
    vals.append(val)

    jethro_metrice_collector.submit_metrics('jethro_mng', 'running_instances', vals)


def submit_maint_status_metrics(jethro_version):
    
    jethro_status_cmd = "service jethro status | awk '/JethroMaint/ {print $5}'"

    # service status prompt has change from version 3.4.2
    if(jethro_version < "3.4.2"):
        jethro_status_cmd = "service jethro status | awk '/JethroMaint/ {print $2}'"

    res = os.popen(jethro_status_cmd)

    instances = []
    for instance in res:
        instance_name = format_instance_name(instance)
        instance_num = instance_name_to_number(instance_name)
        instances.append(instance_num)
    jethro_metrice_collector.submit_metrics('jethro_maint', 'running_maint_services', instances)


def submit_load_scheduler_status_metrics(jethro_version):
    jethro_status_cmd = "service jethro status | awk '/JethroLoadsScheduler/ {print $5}'"

    # service status prompt has change from version 3.4.2
    if(jethro_version < "3.4.2"):
        jethro_status_cmd = "service jethro status | awk '/JethroLoadsScheduler/ {print $2}'"

    res = os.popen(jethro_status_cmd)

    instances = []
    for instance in res:
        instance_name = format_instance_name(instance)
        instance_num = instance_name_to_number(instance_name)
        instances.append(instance_num)
        jethro_metrice_collector.submit_metrics('jethro_load_scheduler', 'running_load_scheduler_services', instances)


def submit_instance_storage_metrics(jethro_user):
    res = os.popen("awk -F \":\" '$1 !~ /#/ {x=$1} {if (x != \"\") print x}' /opt/jethro/instances/services.ini")
    storage_sum = 0.0
    for instance_name in res:
        storage_path = os.popen(
            "awk -F \"=\" '$1 ~ /storage.root.path/ {print $2}' /opt/jethro/instances/" + instance_name.replace('\n', '') + "/local-conf.ini").read()
        storage_usage = os.popen(format('su - {jethro_user} -c "hadoop fs -du -s -h {storage_path}"') +
                                 " | awk '{if ($2 == \"K\") print $1 / 1000 / 1000; else if ($2 == \"M\") print $1 / 1000; else print $1}'").read()
        storage_sum += float(storage_usage)

    vals = []
    vals.append(storage_sum)

    jethro_metrice_collector.submit_metrics(
        'jethro_maint', 'instance_storage_size_gb', vals)

#****************************************************************


#**************** Main Logic *************************

METRICS_INTERVAL = 60

ams_address = sys.argv[1]
jethro_user = sys.argv[2]
jethro_version = sys.argv[3]
jethro_metrice_collector = JethroMetrics(ams_address)
script_dir = os.path.dirname(os.path.abspath(__file__))
init_path = format('{script_dir}/../ams_host.ini')
ams_host = ams_address.split(':')[0]
ams_port = int(ams_address.split(':')[1])

while True:
    try:

        # Writ ams_host to file, so the alerts using these metrics will be able to query AMS.
        # I couldn't find any other alternative :-(
        if not os.path.exists(init_path):
            os.popen('echo ' + ams_host + ' > ' + init_path)

        # Submit metrics
        submit_attached_instances_names_metrics()
        submit_maint_status_metrics(jethro_version)
        submit_load_scheduler_status_metrics(jethro_version)
        submit_running_instances_names_metrics(jethro_version)
        submit_running_instances_metrics()
        submit_instance_storage_metrics(jethro_user)

    except Exception as e:
        print("Unable to submit Jethro metrics to Ambari Metric Collector: " + str(e))
    finally:
        time.sleep(METRICS_INTERVAL)
