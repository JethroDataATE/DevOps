#!/usr/bin/env python

from resource_management.libraries.functions import default
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions.format import format
from resource_management.libraries.script.script import Script

config = Script.get_config()

java64_home = config['hostLevelParams']['java_home']
hostname = config['hostname']
security_enabled = config['configurations']['cluster-env']['security_enabled']
kinit_path = get_kinit_path(
    default('/configurations/kerberos-env/executable_search_paths', None))
kerberos_realm = default('/configurations/kerberos-env/realm', None)
cluster_name = str(config['clusterName']).lower()


jethro_config = config['configurations']['jethro-config']

jethro_kerberos_prinicipal = config['configurations']['jethro-env']['jethro.kerberos.principal']
jethro_kerberos_keytab = config['configurations']['jethro-env']['jethro.kerberos.keytab']

jethro_user = jethro_config['jethro_user']

if security_enabled and (jethro_kerberos_prinicipal == 'none'):
    jethro_kerberos_prinicipal = format('{jethro_user}-{cluster_name}@{kerberos_realm}')
    jethro_kerberos_keytab = "/etc/security/keytabs/jethro.headless.keytab"

jethromng_rpm_name = jethro_config['jethromng_rpm_name']
jethro_rpm_name = jethro_config['jethro_rpm_name']
jethro_instance_name = jethro_config['jethro_instance_name']
jethro_instance_storage_path = jethro_config['jethro_instance_storage_path']
