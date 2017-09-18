#!/usr/bin/env python

from resource_management.core.resources.system import Execute
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.check_process_status import check_process_status


def service_stop(service_name):
    import params
    Execute(
        ("service", service_name, "stop"),
        user=params.jethro_user
    )

def service_start(service_name):
    import params
    Execute(
        ("service", service_name, "start"),
        user=params.jethro_user
    )

def service_status(service_pid_file):
    return check_process_status(service_pid_file)
