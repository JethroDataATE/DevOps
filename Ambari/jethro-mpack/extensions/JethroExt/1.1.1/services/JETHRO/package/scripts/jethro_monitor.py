#!/usr/bin/env python

from resource_management.core.source import StaticFile
from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import File, Execute
from resource_management.core.logger import Logger
from resource_management.libraries.functions.format import format
from jethro_metrics_utils import start_metrics
from jethro_service_utils import setup_kerberos_params, installJethroComponent
from resource_management.libraries.functions.check_process_status import check_process_status


class JethroMonitor(Script):

    JETHRO_SERVICE_NAME = "monitor"

    # ************************ Script Interface methrods ***************************

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)

        Logger.info("Install Jethro Monitor")

        installJethroComponent(params.jethro_rpm_path, params.jethro_user, params.jethro_group)

    def start(self, env):
        import params
        env.set_params(params)

        if params.security_enabled:
            setup_kerberos_params(params.jethro_kerberos_prinicipal,
                                  params.jethro_kerberos_keytab, params.jethro_user)

        Execute(
            ("service", "jethro", "start",
             "host", self.JETHRO_SERVICE_NAME),
            user=params.jethro_user
        )

        self.configure(env)

        start_metrics(params.ams_collector_address, params.jethro_user)

    def stop(self, env):
        import params
        env.set_params(params)

        Execute(
            ("service", "jethro", "stop",
             "host", self.JETHRO_SERVICE_NAME),
            user=params.jethro_user
        )

    def status(self, env):
        import status_params
        env.set_params(status_params)

        if status_params.jethromonitor_pid_file is not None:
            return check_process_status(status_params.jethromonitor_pid_file)
        else:
            return check_process_status('')

    def configure(self, env):
        import params
        env.set_params(params)


if __name__ == "__main__":
    JethroMonitor().execute()
