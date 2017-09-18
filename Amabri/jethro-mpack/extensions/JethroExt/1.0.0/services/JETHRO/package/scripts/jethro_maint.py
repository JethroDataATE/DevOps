#!/usr/bin/env python

from resource_management import *
from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import File, Execute
from resource_management.libraries.functions.format import format

from service_utils import service_start, service_stop, service_status


class JethroMaint(Script):
    JETHRO_SERVICE_NAME = "JethroMaint"

    def install(self, env):
        import params
        env.set_params(params)
        File(
            format("/tmp/{jethro_rpm_name}"),
            content=StaticFile(params.jethro_rpm_name)
        )
        # self.install_packages(env)
        print(format("Install Jethro service: {self.JETHRO_SERVICE_NAME}"))
        rpm_full_path = format("/tmp/{jethro_rpm_name}")
        Execute(
            ("rpm", "-Uvh", rpm_full_path),
            sudo=True
        )

    def stop(self, env):
        import params
        env.set_params(params)
        print(format("Stop Jethro service: {self.JETHRO_SERVICE_NAME}"))
        service_stop(self.JETHRO_SERVICE_NAME)

    def start(self, env):
        import params
        env.set_params(params)
        print(format("Start Jethro service: {self.JETHRO_SERVICE_NAME}"))
        service_stop(self.JETHRO_SERVICE_NAME)

    def status(self, env):
        import params
        env.set_params(params)
        print(format("Status of Jethro service: {self.JETHRO_SERVICE_NAME}"))
        return service_status(params.jethromaint_pid_file)

    def configure(self, env):
        print(format("Configure Jethro service: {self.JETHRO_SERVICE_NAME}"))
        import params
        env.set_params(params)
        self.configure(env)


if __name__ == "__main__":
    JethroMaint().execute()
