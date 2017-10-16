#!/usr/bin/env python

import imp
from resource_management.core.source import StaticFile
from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import File, Execute
from resource_management.libraries.functions.format import format
from jethro_service_utils import create_attach_instance, setup_kerberos, installJethroComponent, ensure_kerberos_tickets
from resource_management.libraries.functions.check_process_status import check_process_status


class JethroMaint(Script):

    JETHRO_SERVICE_NAME = "maint"

    # ************************ Script Interface methrods ***************************

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)

        print("Install Jethro Server")

        installJethroComponent(params.jethro_rpm_path)

        if not params.security_enabled:
            self.ensure_instance_attached()

    def start(self, env):
        import params
        env.set_params(params)

        if params.security_enabled and params.jethro_current_instance_name is None:
            setup_kerberos(params.kinit_path, params.jethro_kerberos_prinicipal,
                           params.jethro_kerberos_keytab, params.jethro_user)

            self.ensure_instance_attached()
            imp.reload(params)

        Execute(
            ("service", "jethro", "start",
             params.jethro_current_instance_name, self.JETHRO_SERVICE_NAME),
            user=params.jethro_user
        )

        self.configure(env)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(
            ("service", "jethro", "stop",
             params.jethro_current_instance_name, self.JETHRO_SERVICE_NAME),
            user=params.jethro_user
        )

    def status(self, env):
        import status_params
        env.set_params(status_params)

        import params
        if params.security_enabled:
            ensure_kerberos_tickets(params.klist_path, params.kinit_path, params.jethro_kerberos_prinicipal,
                                    params.jethro_kerberos_keytab, params.jethro_user)

        return check_process_status(status_params.jethromaint_pid_file)

    def configure(self, env):
        import params
        env.set_params(params)

    # ************************ Private methrods ***************************

    def ensure_instance_attached(self):
        import params
        create_attach_instance(
            self.JETHRO_SERVICE_NAME,
            params.jethro_default_instance_name,
            params.jethro_default_instance_storage_path,
            params.jethro_user
        )


if __name__ == "__main__":
    JethroMaint().execute()
