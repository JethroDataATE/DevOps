#!/usr/bin/env python

from resource_management.libraries.script.script import Script

config = Script.get_config()
jethro_config = config['configurations']['jethro-env']
jethromng_pid_file = jethro_config['jethromng_pid_file']
