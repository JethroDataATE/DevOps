#!/usr/bin/env python

from resource_management.libraries.functions import default
from resource_management.libraries.functions import get_kinit_path, get_klist_path
from resource_management.libraries.functions.format import format
from resource_management.core import shell
from resource_management.libraries.script.script import Script

config = Script.get_config()

# Global config properties
java64_home = config['hostLevelParams']['java_home']
hostname = config['hostname']
cluster_name = str(config['clusterName']).lower()
ams_collector_address =  config['configurations']['ams-site']['timeline.metrics.service.webapp.address']

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


if security_enabled and (jethro_kerberos_prinicipal == 'none'):
    jethro_kerberos_prinicipal = format(
        '{jethro_user}-{cluster_name}@{kerberos_realm}')
    jethro_kerberos_keytab = "/etc/security/keytabs/jethro.headless.keytab"

# Jethro specific properties
jethro_config = config['configurations'].get('jethro-config')
if jethro_config is not None:
    jethromng_rpm_path = jethro_config['jethromng_rpm_path']
    jethro_rpm_path = jethro_config['jethro_rpm_path']
    jethro_default_instance_name = jethro_config['jethro_default_instance_name']
    jethro_default_instance_storage_path = jethro_config['jethro_default_instance_storage_path']

jethro_current_instance_name = None
get_current_instance_cmd = "awk -F \":\" '$1 !~ /#/ {x=$1} END{print x}' /opt/jethro/instances/services.ini"
code, out = shell.call(get_current_instance_cmd)
if code == 0 and out != '':
    jethro_current_instance_name = out
