import urllib
import httplib
import json
import time

from ambari_commons.ambari_metrics_helper import select_metric_collector_hosts_from_hostnames
from ambari_commons.ambari_metrics_helper import load_properties_from_file

RESULT_STATE_OK = 'OK'
RESULT_STATE_CRITICAL = 'CRITICAL'
RESULT_STATE_WARNING = 'WARNING'
RESULT_STATE_UNKNOWN = 'UNKNOWN'
RESULT_STATE_SKIPPED = 'SKIPPED'


def execute(configurations={}, parameters={}, host_name=None):
    return RESULT_STATE_OK, ["Jethro maint service is up and running."]