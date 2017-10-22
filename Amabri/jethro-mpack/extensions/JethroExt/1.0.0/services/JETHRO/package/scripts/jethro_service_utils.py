#!/usr/bin/env python
from resource_management.core.source import StaticFile
from resource_management.libraries.functions.format import format
from resource_management.core.resources.system import File, Execute
from resource_management.core import shell
from resource_management.libraries.script.script import Script


def installJethroComponent(rpm_path):

    script_path = "/tmp/installJethroComponent.sh"

    File(
        script_path,
        content=StaticFile("installJethroComponent.sh")
    )

    Execute(
        ("sh",
         script_path,
         rpm_path),
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
    return format('set global {param_name}={param_value};\n')
    
def exec_jethro_client_command_file(command_file_path, command_file_output):
    import params
    jethro_client_cmd = format('JethroClient {get_current_instance_name()} 127.0.0.1:{get_current_instance_port()} -u {params.jethro_user} -p {params.jethro_password} -i {command_file_path} -c -d '|' > {command_file_output}')
    code, out = shell.call(jethro_client_cmd)

    # code 0 means success, anything else is error.
    return code