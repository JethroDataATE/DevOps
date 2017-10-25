#!/usr/bin/env python
from resource_management.core.source import StaticFile
from resource_management.libraries.functions.format import format
from resource_management.core.resources.system import File, Execute
from resource_management.core import shell
from resource_management.libraries.script.script import Script
import os


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


def create_attach_instance(service_name, instance_name, storage_path, jethro_user):
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
    if shell.call(klist_cmd, user=local_user_name)[0] != 0:
        setup_kerberos(kinit_path, principal_name,
                       keytab_path, local_user_name)


# Read last entry from services.ini and fetch instance name
def get_current_instance_name():
    jethro_current_instance_name = None
    get_current_instance_cmd = "awk -F \":\" '$1 !~ /#/ {x=$1} END{print x}' /opt/jethro/instances/services.ini"
    code, out = shell.call(get_current_instance_cmd)
    if code == 0 and out != '':
        jethro_current_instance_name = out
    return jethro_current_instance_name

# Read attached instances info from services.ini and fetch instance names


def get_locally_attached_instances():
    instances = []
    get_all_instance_cmd = "awk -F \":\" '$1 !~ /#/ {x=$1} {print x}' /opt/jethro/instances/services.ini"
    res = os.popen(get_all_instance_cmd)
    for instance in res:
        trim_inst = instance.replace('LF', '').strip()
        if trim_inst != '' and trim_inst not in instances:
            instances.append(trim_inst)
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
        "/ {x=$" + service_index + "} END{print x}' /opt/jethro/instances/services.ini"
    code, out = shell.call(get_service_config_cmd)
    if code == 0 and out != '':
        service_installed = (out == 'yes')
    return service_installed


# Read last entry from services.ini and fetch instance port
def get_current_instance_port():
    jethro_current_instance_port = None
    get_current_instance_port_cmd = "awk -F \":\" '$1 !~ /#/ {x=$2} END{print x}' /opt/jethro/instances/services.ini"
    code, out = shell.call(get_current_instance_port_cmd)
    if code == 0 and out != '':
        jethro_current_instance_port = out
    return jethro_current_instance_port


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
    jethro_client_cmd = format("JethroClient {inst_name} 127.0.0.1:{inst_port} -u {params.jethro_user} -p {params.jethro_password} -i {command_file_path} -c -d '|'")
    print (format('Set params command: {jethro_client_cmd}'))
    
    try:
        with open(command_file_path, 'r') as cmd_file:
            cmd_content = cmd_file.read()
            print (format('Commands: {cmd_content}'))
    except Exception as e:
        print (format('Fail to read commands file: {e}'))
    
    code, out = shell.call(jethro_client_cmd)
    if code == 0:
        print (format('Success changing global Jethro paramaters:\n{out}'))
    else:
        print (format('Failed changing global Jethro paramaters:\n{out}'))

    shell.call(format('rm -f {command_file_path}'))