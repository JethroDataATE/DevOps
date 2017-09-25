#!/usr/bin/env python

from resource_management.libraries.functions import default
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.script.script import Script

config = Script.get_config()

java64_home = config['hostLevelParams']['java_home']
hostname = config['hostname']
security_enabled = config['configurations']['cluster-env']['security_enabled']
kinit_path_local = get_kinit_path(
    default('/configurations/kerberos-env/executable_search_paths', None))

jethro_config = config['configurations']['jethro-config']
jethromng_rpm_name = jethro_config['jethromng_rpm_name']
jethro_rpm_name = jethro_config['jethro_rpm_name']
jethro_user = jethro_config['jethro_user']
jethro_instance_name = jethro_config['jethro_instance_name']
jethro_instance_storage_path = jethro_config['jethro_instance_storage_path']
