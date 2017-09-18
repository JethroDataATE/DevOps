#!/usr/bin/env python

from resource_management.libraries.script.script import Script

config = Script.get_config()

java64_home = config['hostLevelParams']['java_home']
hostname = config['hostname']
jethro_config = config['configurations']['jethro-config']
jethromng_rpm_name = jethro_config['jethromng_rpm_name']
jethro_rpm_name = jethro_config['jethro_rpm_name']
jethro_user = jethro_config['jethro_user']
jethro_instance_name = jethro_config['jethro_instance_name']
jethro_instance_storage_path = jethro_config['jethro_instance_storage_path']
