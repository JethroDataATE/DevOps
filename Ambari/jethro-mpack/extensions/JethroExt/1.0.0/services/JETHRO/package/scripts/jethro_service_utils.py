#!/usr/bin/env python

from resource_management.core.source import StaticFile
from resource_management.libraries.functions.format import format
from resource_management.core.resources.system import File, Execute
from resource_management.core import shell
from resource_management.libraries.script.script import Script
import os
from resource_management.core.logger import Logger


SERVICES_INI = "/opt/jethro/instances/services.ini"


def installJethroComponent(rpm_path, jethro_user):

    script_path = "/tmp/installJethroComponent.sh"

    File(
        script_path,
        content=StaticFile("installJethroComponent.sh")
    )

    Execute(
        ("sh",
         script_path,
         rpm_path,
         jethro_user),
        sudo=True
    )

    # Cleanup
    Execute(
        ("rm",
         "-f",
         script_path),
        sudo=True
    )


def create_attach_instance(service_name, instance_name, storage_path, cache_path, cache_size, jethro_user):
    import params

    script_path = "/tmp/ensureJethroInstance.sh"

    # Copy installation script
    File(
        script_path,
        content=StaticFile("ensureJethroInstance.sh")
    )

    # Execute script
    Execute(
        ("sh",
         script_path,
         service_name,
         instance_name,
         storage_path,
         cache_path,
         cache_size,
         jethro_user),
        tries=3,
        try_sleep=3,
        sudo=True
    )

    # Cleanup
    Execute(
        ("rm",
         "-f",
         script_path),
        sudo=True
    )


def setup_kerberos(kinit_path, principal_name, keytab_path, local_user_name):
    Execute(
        (kinit_path,
         "-kt",
         keytab_path, principal_name),
        user=local_user_name
    )


def ensure_kerberos_tickets(klist_path, kinit_path, principal_name, keytab_path, local_user_name):
    # If there are no tickets in the cache or they are expired, perform a kinit, else use what is in the cache
    klist_cmd = format("{klist_path} -s")
    if shell.call(klist_cmd, user=local_user_name, timeout=20)[0] != 0:
        Logger.debug("Renewing Jethro kerberso tickets.")
        setup_kerberos(kinit_path, principal_name,
                       keytab_path, local_user_name)


def get_instance_details():
    jethro_current_instance_name = None
    jethro_current_instance_port = None

    # read all rows in services.ini
    with open(SERVICES_INI, 'r') as services_ini:
        content = services_ini.read()
        instances = content.split('\n')
        if instances is not None and len(instances) > 1:
            # read the last entry on the array
            last_inst = instances[len(instances) - 2]
            last_inst_parts = last_inst.split(':')
            if len(last_inst_parts) > 2 and not last_inst_parts[0].startswith('#'):
                jethro_current_instance_name = last_inst_parts[0]
                jethro_current_instance_port = last_inst_parts[1]

    Logger.debug("Jethro instance details: {0}.".format(jethro_current_instance_name))
    return jethro_current_instance_name, jethro_current_instance_port

# Read last entry from services.ini and fetch instance name
def get_current_instance_name():
    return get_instance_details()[0]


# Read last entry from services.ini and fetch instance port
def get_current_instance_port():
    return get_instance_details()[1]


# Read attached instances info from services.ini and fetch instance names
def get_locally_attached_instances():
    instances = []
    with open(SERVICES_INI, 'r') as services_ini:
        content = services_ini.read()
        instances_data = content.split('\n')
        for instance in instances_data:
            trim_inst = instance.replace('LF', '').strip()
            if trim_inst != '' and not trim_inst.startswith('#'):
                instance_parts = trim_inst.split(':')
                instance_name = instance_parts[0]
                if instance_name not in instances:
                    instances.append(instance_name)
    return instances

# Read service config from services.ini for specific instance
def is_service_installed_for_instance(instance_name, service_name):
    service_installed = False

    # Set service index in services.ini
    service_index = '3'
    if service_name == 'maint':
        service_index = '4'
    elif service_name == 'loadscheduler':
        service_index = '5'

    get_service_config_cmd = "awk -F \":\" '$1 ~ /" + instance_name + \
        "/ {x=$" + service_index + "} END{print x}' " + SERVICES_INI
    code, out = shell.call(get_service_config_cmd, timeout=20)
    if code == 0 and out != '':
        service_installed = (out == 'yes')
    return service_installed


def set_param_command(config_name, param_name):
    config = Script.get_config()
    param_value = None
    config_type = config['configurations'].get(config_name)
    if config_type is not None:
        param_value = config_type[param_name]

    # change boolean values to 0,1 for Jethro compatibility.
    if param_value == True:
        param_value = 1

    if param_value == False:
        param_value = 0
    # ----------------------------------------------------

    return format('set global {param_name}={param_value};\n')


def exec_jethro_client_command_file(command_file_path):
    import params
    inst_name = get_current_instance_name()
    inst_port = get_current_instance_port()
    jethro_client_cmd = format(
        "JethroClient {inst_name} 127.0.0.1:{inst_port} -u {params.jethro_user} -p {params.jethro_password} -i {command_file_path} -c -d '|'")
    Logger.debug("Set params command: {0}".format(jethro_client_cmd))

    try:
        with open(command_file_path, 'r') as cmd_file:
            cmd_content = cmd_file.read()
            print(format('Commands: {cmd_content}'))
    except Exception as e:
       Logger.error("Fail to read commands file: {0}".format(e))

    code, out = shell.call(jethro_client_cmd, timeout=60)
    if code == 0:
        Logger.info("Success changing global Jethro paramaters:\n{0}".format(out))
    else:
        Logger.error("Failed changing global Jethro paramaters:\n{0}".format(out))

    shell.call(format('rm -f {command_file_path}'), timeout=20)
