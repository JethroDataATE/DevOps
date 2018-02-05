import json
import time
import urllib
import os
import subprocess
import sys
from resource_management.libraries.functions.format import format
import ambari_commons.network as network

def start_metrics(ams_collector_address, jethro_user, jethro_version):
    
    # If jethro metrics process is already running on this host - do nothing
    running_metrics = os.popen("COLUMNS=20000 ps ax | grep jethro_metrics | grep -v grep").read()
    if running_metrics != '':
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = format('{script_dir}/jethro_metrics.py')
    subprocess.Popen(['python', script_path, ams_collector_address, jethro_user, jethro_version, ' &'])

def stop_metrics():
    for line in os.popen("COLUMNS=20000 ps ax | grep jethro_metrics | grep -v grep"):
        fields = line.split()
        pid = fields[0]
        os.kill(int(pid), 15)


def instance_name_to_number(instance_name):
    max_len = int(len(str(sys.maxsize)) / 2)
    upper_str = instance_name.replace('\n', '').upper()
    chars = []
    for c in upper_str:
        str_c = str(ord(c))
        if str_c != 10:
            chars.append(str_c)
        if (len(chars) - 1) == max_len:
            break

    str_val = ''.join(chars)
    val = int(str_val)
    return val

def instance_number_to_name(instance_number):
    instance_str = str(int(instance_number))
    chars = []
    x = 0
    while x < len(instance_str):
        c_a = instance_str[x]
        c_b = instance_str[x+1]
        ascii_val = int(c_a + c_b)
        char = chr(ascii_val)
        chars.append(char)
        x += 2

    instance_name = ''.join(chars)
    return instance_name
    

def read_metric_values(collector_host, collector_port, metric_collector_https_enabled, app_id, metric_name, interval = 1):

    current_time = int(time.time()) * 1000

    ams_monitor_conf_dir = "/etc/ambari-metrics-monitor/conf"
    metric_truststore_ca_certs = 'ca.pem'
    ca_certs = os.path.join(ams_monitor_conf_dir, metric_truststore_ca_certs)

    AMS_METRICS_GET_URL = "/ws/v1/timeline/metrics?%s"

    get_metrics_parameters = {
        "metricNames": metric_name,
        "appId": app_id,
        "hostname": "%",
        "precision": "seconds",
        "startTime": current_time - interval * 60 * 1000,
        "endTime": current_time,
        "grouped": "true",
    }

    encoded_get_metrics_parameters = urllib.urlencode(get_metrics_parameters)

    
    try:
        conn = network.get_http_connection(collector_host, collector_port, metric_collector_https_enabled, ca_certs)
        conn.request("GET", AMS_METRICS_GET_URL %
                     encoded_get_metrics_parameters)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("Unable to retrive Jethro metrics information.", e)
        return None

    if response.status != 200:
        print("Failed to retrive Jethro metrics information.")
        return None

    data_json = json.loads(data)
    metrics = []

    for metrics_data in data_json["metrics"]:
        metrics += metrics_data["metrics"].values()
    pass

    return metrics
