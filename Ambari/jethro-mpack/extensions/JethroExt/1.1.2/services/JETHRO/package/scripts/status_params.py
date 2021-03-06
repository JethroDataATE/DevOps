#!/usr/bin/env python

from resource_management.libraries.functions.format import format
from resource_management.libraries.script.script import Script
from jethro_service_utils import get_current_instance_name

config = Script.get_config()
jethro_config = config['configurations']['jethro-env']

jethro_instance_name = None
jethroloadschedule_pid_file = None
jethroserver_pid_file = None
jethromaint_pid_file = None
jethro_pid_dir = jethro_config['jethro_pid_dir']
jethromonitor_pid_file =  format('{jethro_pid_dir}/JethroMonitor.pid')

jethro_instance_name = get_current_instance_name()
if jethro_instance_name is not None:   
    jethroloadschedule_pid_file = format(
        '{jethro_pid_dir}/jethroloadscheduler_{jethro_instance_name}.pid')
    jethroserver_pid_file = format(
        '{jethro_pid_dir}/jethroserver_{jethro_instance_name}.pid')
    jethromaint_pid_file = format(
        '{jethro_pid_dir}/jethromaint_{jethro_instance_name}.pid')
