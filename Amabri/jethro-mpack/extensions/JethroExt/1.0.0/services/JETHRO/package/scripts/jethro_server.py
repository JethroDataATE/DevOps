#!/usr/bin/env python

from resource_management import *
from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import File, Execute
from resource_management.libraries.functions.format import format

from service_utils import service_start, service_stop, service_status


class JethroServer(Script):
    JETHRO_SERVICE_NAME = "jethro"

    def install(self, env):
        import params
        env.set_params(params)

        # Installing jethro rpm
        File(
            format("/tmp/{jethro_rpm_name}"),
            content=StaticFile(params.jethro_rpm_name)
        )
        self.install_packages(env)
        print("Install Jethro Server")
        rpm_full_path = format("/tmp/{jethro_rpm_name}")
        Execute(
            ("rpm", "-Uvh", rpm_full_path),
            sudo=True
        )

        # Create/Attach instance
        File(
            format("/tmp/createAttachInstance.sh"),
            content=StaticFile("createAttachInstance.sh")
        )
        print("Create/Attach Jethro Instance...")
        script_path = format("/tmp/createAttachInstance.sh")
        Execute(
            ("sh", script_path, params.jethro_instance_name,
             params.jethro_instance_storage_path),
            sudo=True
        )

    def start(self, env):
        import params
        env.set_params(params)
        # print(format("Start Jethro service: {JETHRO_SERVICE_NAME}"))
        service_start(self.JETHRO_SERVICE_NAME)
        self.configure(env)

    def stop(self, env):
        import params
        env.set_params(params)
        # print(format("Stop Jethro service: {JETHRO_SERVICE_NAME}"))
        service_stop(self.JETHRO_SERVICE_NAME)

    def status(self, env):
        import status_params
        env.set_params(status_params)
        # print(format("Status of Jethro service: {JETHRO_SERVICE_NAME}"))
        return service_status(status_params.jethroserver_pid_file)

    def configure(self, env):
        # print(format("Configure Jethro service: {JETHRO_SERVICE_NAME}"))
        import params
        env.set_params(params)


if __name__ == "__main__":
    JethroServer().execute()
