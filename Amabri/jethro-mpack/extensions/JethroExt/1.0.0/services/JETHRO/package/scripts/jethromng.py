#!/usr/bin/env python

from resource_management import *
from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import File, Execute
from resource_management.libraries.functions.format import format

from service_utils import service_start, service_stop, service_status


class JethroMng(Script):
    JETHROMNG_SERVICE_NAME = "jethromng"

    def install(self, env):
        import params
        env.set_params(params)
        File(
            format("/tmp/{jethromng_rpm_name}"),
            content=StaticFile(params.jethromng_rpm_name)
        )
        self.install_packages(env)
        print('Install Jethro Manager')
        rpm_full_path = format("/tmp/{jethromng_rpm_name}")
        Execute(
            ("rpm", "-Uvh", rpm_full_path),
            sudo=True
        )

    def start(self, env):
        import params
        env.set_params(params)
        print('Start the Jethro Manager')
        service_start(self.JETHROMNG_SERVICE_NAME)
        self.configure(env)

    def stop(self, env):
        import params
        env.set_params(params)
        print('Stop the Jethro Manager')
        service_stop(self.JETHROMNG_SERVICE_NAME)

    def status(self, env):
        import status_params
        env.set_params(status_params)
        print('Status of the Jethro Manager')
        return service_status(status_params.jethromng_pid_file)

    def configure(self, env):
        print('Configure the Jethro Manager')
        import params
        env.set_params(params)


if __name__ == "__main__":
    JethroMng().execute()
