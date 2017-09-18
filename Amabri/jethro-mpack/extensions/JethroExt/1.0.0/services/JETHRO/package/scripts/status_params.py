#!/usr/bin/env python

from resource_management.libraries.functions.format import format
from resource_management.libraries.script.script import Script

config = Script.get_config()

jethro_config = config['configurations']['jethro-config']


jethromng_pid_file = jethro_config['jethromng_pid_file']

jethro_instance_name = jethro_config['jethro_instance_name']
jethro_pid_dir = jethro_config['jethro_pid_dir']

jethroloadschedule_pid_file = format('{jethro_pid_dir}/jethroloadscheduler_{jethro_instance_name}.pid')
jethroserver_pid_file = format('{jethro_pid_dir}/jethroserver_{jethro_instance_name}.pid')
jethromaint_pid_file = format('{jethro_pid_dir}/jethromaint_{jethro_instance_name}.pid')
