#!/usr/bin/env python

from resource_management import *
from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import File, Execute
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.check_process_status import check_process_status


class JethroServer(Script):
    JETHRO_SERVICE_NAME = "server"

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)

        print("Install Jethro Server")

        # Copy jethro rpm
        rpm_full_path = format("/tmp/{jethro_rpm_name}")
        File(
            rpm_full_path,
            content=StaticFile(params.jethro_rpm_name)
        )

        # Copy installation script
        File(
            format("/tmp/installJethroService.sh"),
            content=StaticFile("installJethroService.sh")
        )
        script_path = format("/tmp/installJethroService.sh")
        Execute(
            ("sh",
             script_path,
             params.jethro_rpm_name,
             self.JETHRO_SERVICE_NAME,
             params.jethro_instance_name,
             params.jethro_instance_storage_path),
            tries=3,
            try_sleep=3,
            sudo=True
        )

    def start(self, env):
        import params
        env.set_params(params)
        Execute(
            ("service", "jethro", "start", params.jethro_instance_name),
            user=params.jethro_user
        )

        # Set current instance
        File(
            "/opt/jethro/cur_inst",
            content=params.jethro_instance_name
        )

        self.configure(env)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(
            ("service", "jethro", "stop", params.jethro_instance_name),
            user=params.jethro_user
        )

    def status(self, env):
        import status_params
        env.set_params(status_params)
        return check_process_status(status_params.jethroserver_pid_file)

    def configure(self, env):
        import params
        env.set_params(params)


if __name__ == "__main__":
    JethroServer().execute()
