#!/usr/bin/env python

from resource_management.core.source import StaticFile
from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import File, Execute
from resource_management.libraries.functions.format import format
from jethro_service_utils import create_attach_instance
from resource_management.libraries.functions.check_process_status import check_process_status


class JethroMaint(Script):
    JETHRO_SERVICE_NAME = "maint"

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)

        print("Install Jethro Server")

        # Install jethro rpm
        rpm_full_path = format("/tmp/{jethro_rpm_name}")
        File(
            rpm_full_path,
            content=StaticFile(params.jethro_rpm_name)
        )
        Execute(
            ("rpm", "-Uvh", "--force", rpm_full_path),
            sudo=True
        )

        if not params.security_enabled:
            create_attach_instance(
                self.JETHRO_SERVICE_NAME, params.jethro_instance_name, params.jethro_instance_storage_path)

    def start(self, env):
        import params
        env.set_params(params)

        if params.security_enabled:
            Execute(
                   ("kinit", "-k", "-t",
                    "/etc/security/keytabs/jethro.headless.keytab", params.jethro_user),
                user=params.jethro_user
            )

            create_attach_instance(
                self.JETHRO_SERVICE_NAME, params.jethro_instance_name, params.jethro_instance_storage_path)

        Execute(
            ("service", "jethro", "start",
             params.jethro_instance_name, self.JETHRO_SERVICE_NAME),
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
            ("service", "jethro", "stop",
             params.jethro_instance_name, self.JETHRO_SERVICE_NAME),
            user=params.jethro_user
        )

    def status(self, env):
        import status_params
        env.set_params(status_params)
        return check_process_status(status_params.jethromaint_pid_file)

    def configure(self, env):
        import params
        env.set_params(params)


if __name__ == "__main__":
    JethroMaint().execute()
