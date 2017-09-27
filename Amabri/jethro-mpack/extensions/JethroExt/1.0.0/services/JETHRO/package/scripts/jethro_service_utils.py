#!/usr/bin/env python
from resource_management.core.source import StaticFile
from resource_management.libraries.functions.format import format
from resource_management.core.resources.system import File, Execute


def create_attach_instance(service_name, instance_name, storage_path):
    import params
    # Copy installation script
    File(
        format("/tmp/installJethroService.sh"),
        content=StaticFile("installJethroService.sh")
    )
    script_path = format("/tmp/installJethroService.sh")
    Execute(
        ("sh",
         script_path,
         service_name,
         instance_name,
         storage_path),
        tries=3,
        try_sleep=3,
        sudo=True
    )
