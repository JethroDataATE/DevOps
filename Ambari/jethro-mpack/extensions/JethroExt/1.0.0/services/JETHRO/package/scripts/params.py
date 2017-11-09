#!/usr/bin/env python

from resource_management.libraries.functions import default
from resource_management.libraries.functions import get_kinit_path, get_klist_path
from resource_management.libraries.functions.format import format
from resource_management.libraries.script.script import Script
from ambari_commons.ambari_metrics_helper import select_metric_collector_hosts_from_hostnames

config = Script.get_config()

# Global config properties
# java64_home = config['hostLevelParams']['java_home']
HOSTNAME = config['hostname']
CLUSTER_NAME = str(config['clusterName']).lower()
# ams_collector_address =  config['configurations']['ams-site']['timeline.metrics.service.webapp.address']
ams_collector_hosts = ",".join(
    default("/clusterHostInfo/metrics_collector_hosts", []))

if 'cluster-env' in config['configurations'] and \
        'metrics_collector_external_hosts' in config['configurations']['cluster-env']:
    ams_collector_hosts = config['configurations']['cluster-env']['metrics_collector_external_hosts']
else:
    ams_collector_hosts = ",".join(
        default("/clusterHostInfo/metrics_collector_hosts", []))

metric_collector_host = select_metric_collector_hosts_from_hostnames(
    ams_collector_hosts)

metric_collector_port = '6188'
if 'cluster-env' in config['configurations'] and \
        'metrics_collector_external_port' in config['configurations']['cluster-env']:
    metric_collector_port = config['configurations']['cluster-env']['metrics_collector_external_port']
else:
    metric_collector_web_address = default(
        "/configurations/ams-site/timeline.metrics.service.webapp.address", "0.0.0.0:6188")
    if metric_collector_web_address.find(':') != -1:
        metric_collector_port = metric_collector_web_address.split(':')[1]

ams_collector_address = format('{metric_collector_host}:{metric_collector_port}')

# Security Properties
security_enabled = config['configurations']['cluster-env']['security_enabled']
kinit_path = get_kinit_path(
    default('/configurations/kerberos-env/executable_search_paths', None))
klist_path = get_klist_path(
    default('/configurations/kerberos-env/executable_search_paths', None))
kerberos_realm = default('/configurations/kerberos-env/realm', None)
jethro_kerberos_prinicipal = config['configurations']['jethro-env']['jethro.kerberos.principal']
jethro_kerberos_keytab = config['configurations']['jethro-env']['jethro.kerberos.keytab']
jethro_user = config['configurations']['jethro-env']['jethro_user']
jethro_password = config['configurations']['jethro-env']['jethro_password']

if security_enabled and (jethro_kerberos_prinicipal == 'none'):
    jethro_kerberos_prinicipal = format('{jethro_user}-{CLUSTER_NAME}@{kerberos_realm}')
    jethro_kerberos_keytab = "/etc/security/keytabs/jethro.headless.keytab"

# Jethro specific properties
jethro_config = config['configurations'].get('jethro-config')
if jethro_config is not None:
    jethromng_rpm_path = jethro_config['jethromng_rpm_path']
    jethro_rpm_path = jethro_config['jethro_rpm_path']
    jethro_instance_name = jethro_config['jethro_instance_name']
    jethro_instance_storage_path = jethro_config['jethro_instance_storage_path']
