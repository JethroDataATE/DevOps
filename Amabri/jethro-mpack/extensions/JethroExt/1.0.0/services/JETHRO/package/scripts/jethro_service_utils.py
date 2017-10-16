#!/usr/bin/env python
from resource_management.core.source import StaticFile
from resource_management.libraries.functions.format import format
from resource_management.core.resources.system import File, Execute
from resource_management.core import shell


def installJethroComponent(rpm_path):
    File(
        "/tmp/installJethroComponent.sh",
        content=StaticFile("installJethroComponent.sh")
    )
    Execute(
        ("sh",
         "/tmp/installJethroComponent.sh",
         rpm_path),
        sudo=True
    )


def create_attach_instance(service_name, instance_name, storage_path, jethro_user):
    import params

    # Copy installation script
    File(
        "/tmp/ensureJethroInstance.sh",
        content=StaticFile("ensureJethroInstance.sh")
    )
    script_path = "/tmp/ensureJethroInstance.sh"

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
        setup_kerberos(kinit_path, principal_name, keytab_path, local_user_name)
