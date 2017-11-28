import os
from resource_management.libraries.functions.format import format

RESULT_STATE_OK = 'OK'
RESULT_STATE_CRITICAL = 'CRITICAL'
RESULT_STATE_WARNING = 'WARNING'
RESULT_STATE_UNKNOWN = 'UNKNOWN'
RESULT_STATE_SKIPPED = 'SKIPPED'

AMS_HTTP_POLICY = '{{ams-site/timeline.metrics.service.http.policy}}'
METRICS_COLLECTOR_WEBAPP_ADDRESS_KEY = '{{ams-site/timeline.metrics.service.webapp.address}}'
AMS_METRICS_GET_URL = "/ws/v1/timeline/metrics?%s"

METRIC_NAME_PARAM_KEY = 'metricName'
APP_ID_PARAM_KEY = 'appId'
SERVICE_DISPLAY_NAME_PARAM_KEY = 'serviceDisplayName'

ATTACHED_INSTANCES_APP_ID = 'jethro_mng'
ATTACHED_INSTANCES_METRIC_NAME = 'attached_instances_names'


def get_tokens():
    return (METRICS_COLLECTOR_WEBAPP_ADDRESS_KEY, AMS_HTTP_POLICY)

# load modules dynamically form relative path
def load_src(name, fpath):
    import os
    import imp
    return imp.load_source(name, os.path.join(os.path.dirname(__file__), fpath))


def execute(configurations={}, parameters={}, host_name=None):

    try:
        if METRIC_NAME_PARAM_KEY in parameters:
            metric_name = parameters[METRIC_NAME_PARAM_KEY]

        if APP_ID_PARAM_KEY in parameters:
            app_id = parameters[APP_ID_PARAM_KEY]

        if SERVICE_DISPLAY_NAME_PARAM_KEY in parameters:
            service_name = parameters[SERVICE_DISPLAY_NAME_PARAM_KEY]

        # load jethro_metrics_utils module dynamically
        load_src("jethro_metrics_utils", "../scripts/jethro_metrics_utils.py")
        import jethro_metrics_utils
        from jethro_metrics_utils import read_metric_values, instance_number_to_name, instance_name_to_number

        ams_monitor_conf_dir = "/etc/ambari-metrics-monitor/conf"
        metric_truststore_ca_certs = 'ca.pem'
        ca_certs = os.path.join(ams_monitor_conf_dir,
                                metric_truststore_ca_certs)
        metric_collector_https_enabled = str(
            configurations[AMS_HTTP_POLICY]) == "HTTPS_ONLY"

        script_dir = os.path.dirname(os.path.abspath(__file__))
        init_path = format('{script_dir}/../ams_host.ini')

        with open(init_path, 'r') as ams_host:
            collector_host = ams_host.read().replace('\n', '')

        collector_port = int(
            configurations[METRICS_COLLECTOR_WEBAPP_ADDRESS_KEY].split(':')[1])

        running_services_metrics = read_metric_values(collector_host, collector_port, metric_collector_https_enabled,
                                                      app_id, metric_name, 5)

        if running_services_metrics is None or len(running_services_metrics) == 0:
            return RESULT_STATE_CRITICAL, [format('No Jethro {service_name} service is running.')]

        running_services_metrics = set(running_services_metrics)

        attached_instances_metrics = read_metric_values(
            collector_host, collector_port, metric_collector_https_enabled, ATTACHED_INSTANCES_APP_ID, ATTACHED_INSTANCES_METRIC_NAME)

        attached_instances_numbers = set(attached_instances_metrics)

        # load jethro_service_utils module dynamically
        load_src("jethro_service_utils", "../scripts/jethro_service_utils.py")
        import jethro_service_utils
        from jethro_service_utils import get_locally_attached_instances

        # get locally attached instances
        instances = get_locally_attached_instances()
        local_instances_numbers = []

        # cast names to numbers
        for name in instances:
            number = instance_name_to_number(name)
            local_instances_numbers.append(number)

        alert_msg = ""

        for instance_number in attached_instances_numbers:
            # if instance is attached to this server - raise the alert
            if (instance_number not in running_services_metrics) and (instance_number in local_instances_numbers):
                instance_name = instance_number_to_name(instance_number)
                alert_msg += format('No Jethro {service_name} service is running for instance: {instance_name}.\n')

        if alert_msg == "":
            return RESULT_STATE_OK, [format('Jethro {service_name} service is up and running.')]
        else:
            return RESULT_STATE_CRITICAL, [alert_msg]
    except Exception as e:
        strErr = str(e)
        return RESULT_STATE_UNKNOWN, [format('Unable to determine whethe Jethro {service_name} service is running: {strErr}.')]
