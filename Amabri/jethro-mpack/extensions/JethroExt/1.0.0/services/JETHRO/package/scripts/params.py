#!/usr/bin/env python

import functools

from ambari_commons.ambari_metrics_helper import select_metric_collector_hosts_from_hostnames
from resource_management.libraries.functions import conf_select
from resource_management.libraries.functions import default
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions import stack_select
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources
from resource_management.libraries.resources.hdfs_resource import HdfsResource
from resource_management.libraries.script.script import Script


config = Script.get_config()

java64_home = config['hostLevelParams']['java_home']
hostname = config['hostname']
jethro_config = config['configurations']['jethro-config']
jethromng_rpm_name = jethro_config['jethromng_rpm_name']
jethro_rpm_name = jethro_config['jethro_rpm_name']
jethro_user = jethro_config['jethro_user']