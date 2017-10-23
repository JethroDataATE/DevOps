#!/usr/bin/env python

import imp
import time
from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import File, Execute
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.check_process_status import check_process_status
from jethro_service_utils import create_attach_instance, setup_kerberos, installJethroComponent, ensure_kerberos_tickets, get_current_instance_name, set_param_command, exec_jethro_client_command_file

class JethroServer(Script):

    JETHRO_SERVICE_NAME = "server"
    COMMAND_FILE_PATH = "/tmp/jethro_client_commands.sql"
    COMMAND_FILE_OUTPUT = "/tmp/jethro_client_commands.out"

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

        instance_name = get_current_instance_name()

        if params.security_enabled and instance_name is None:
            setup_kerberos(params.kinit_path, params.jethro_kerberos_prinicipal,
                           params.jethro_kerberos_keytab, params.jethro_user)

            self.ensure_instance_attached()
            imp.reload(params)

        Execute(
            ("service", "jethro", "start", instance_name),
            user=params.jethro_user
        )

        # wait 5 secs for service start before trying to configure.
        time.sleep(5)

        self.configure(env)

    def stop(self, env):
        import params
        env.set_params(params)

        instance_name = get_current_instance_name()

        Execute(
            ("service", "jethro", "stop", instance_name),
            user=params.jethro_user
        )

    def status(self, env):
        import status_params
        env.set_params(status_params)

        import params
        if params.security_enabled:
            ensure_kerberos_tickets(params.klist_path, params.kinit_path, params.jethro_kerberos_prinicipal,
                                    params.jethro_kerberos_keytab, params.jethro_user)

        return check_process_status(status_params.jethroserver_pid_file)

    def configure(self, env):
        import params
        env.set_params(params)

        print 'configure Jethro server called.'

        commands = ""
        commands += set_param_command("jethro-global", "dynamic.aggregation.auto.generate.enable")

        File(self.COMMAND_FILE_PATH, content=commands)

        exec_jethro_client_command_file(self.COMMAND_FILE_PATH, self.COMMAND_FILE_OUTPUT)

    # ************************ Private methods ***************************

    def ensure_instance_attached(self):
        import params
        create_attach_instance(
            self.JETHRO_SERVICE_NAME,
            params.jethro_default_instance_name,
            params.jethro_default_instance_storage_path,
            params.jethro_user
        )


if __name__ == "__main__":
    JethroServer().execute()
