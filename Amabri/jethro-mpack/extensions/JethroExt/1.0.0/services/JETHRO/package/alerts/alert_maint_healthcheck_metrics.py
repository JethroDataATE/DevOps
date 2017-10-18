import httplib
import json
import os
import time
import urllib
from ambari_commons.os_family_impl import OsFamilyFuncImpl, OsFamilyImpl
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.format import format
import ambari_commons.network as network
from ambari_commons.aggregate_functions import sum

# ambari_server_hostname = config['clusterHostInfo']['ambari_server_host'][0]
# ambari_server_port = config['clusterHostInfo']['ambari_server_port'][0]
# ambari_server_address = format('{ambari_server_hostname}:{ambari_server_port}')

RESULT_STATE_OK = 'OK'
RESULT_STATE_CRITICAL = 'CRITICAL'
RESULT_STATE_WARNING = 'WARNING'
RESULT_STATE_UNKNOWN = 'UNKNOWN'
RESULT_STATE_SKIPPED = 'SKIPPED'

AMS_HTTP_POLICY = '{{ams-site/timeline.metrics.service.http.policy}}'
METRICS_COLLECTOR_WEBAPP_ADDRESS_KEY = '{{ams-site/timeline.metrics.service.webapp.address}}'
METRICS_COLLECTOR_WEBAPP_HOST = '{{clusterHostInfo/metrics_collector_hosts}}'
AMS_METRICS_GET_URL = "/ws/v1/timeline/metrics?%s"
APP_ID = 'JETHRO_MAINT'
METRIC_NAME = 'running_maint_services'


def get_tokens():
    return (METRICS_COLLECTOR_WEBAPP_HOST, METRICS_COLLECTOR_WEBAPP_ADDRESS_KEY, AMS_HTTP_POLICY)


def execute(configurations={}, parameters={}, host_name=None):


    metric_name = 'running_maint_services'
    current_time = int(time.time()) * 1000

    ams_monitor_conf_dir = "/etc/ambari-metrics-monitor/conf"
    metric_truststore_ca_certs = 'ca.pem'
    ca_certs = os.path.join(ams_monitor_conf_dir,
                            metric_truststore_ca_certs)
    metric_collector_https_enabled = str(
        configurations[AMS_HTTP_POLICY]) == "HTTPS_ONLY"

    collector_host = configurations[METRICS_COLLECTOR_WEBAPP_HOST]
    collector_port = int(configurations[METRICS_COLLECTOR_WEBAPP_ADDRESS_KEY].split(':')[1])

    get_metrics_parameters = {
        "metricNames": METRIC_NAME,
        "appId": APP_ID,
        "startTime": current_time - 60 * 60 * 1000,
        "endTime": current_time,
        "grouped": "true",
    }

    encoded_get_metrics_parameters = urllib.urlencode(get_metrics_parameters)

    try:
        conn = network.get_http_connection(collector_host, int(collector_port), metric_collector_https_enabled, ca_certs)
        conn.request("GET", AMS_METRICS_GET_URL % encoded_get_metrics_parameters)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("Unable to retrive Jethro Maint information.", e)
        return RESULT_STATE_UNKNOWN, ["Unable to retrive Jethro Maint information." + str(e)]
    
    if response.status != 200:
        return (RESULT_STATE_UNKNOWN, ["Unable to retrieve metrics from the Ambari Metrics service."])

    data_json = json.loads(data)
    metrics = []

    for metrics_data in data_json["metrics"]:
        metrics += metrics_data["metrics"].values()
    pass

    sum_value = sum(metrics)

    if sum_value > 0:
        return RESULT_STATE_OK, ["Jethro Maint service is up and running."]
    else:
        return RESULT_STATE_CRITICAL, ["No Jethro Maint service found."]
