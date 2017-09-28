#!/usr/bin/env python

from resource_management.core.source import StaticFile
from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import File, Execute
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.check_process_status import check_process_status
from jethro_service_utils import create_attach_instance, setup_kerberos
from jethro_metrics import JethroMetrics


class JethroServer(Script):

    JETHRO_SERVICE_NAME = "server"

    # ************************ Script Interface methrods ***************************

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
            self.ensure_instance_attached()

    def start(self, env):
        import params
        env.set_params(params)

        if params.security_enabled:
            setup_kerberos(params.kinit_path, params.jethro_kerberos_prinicipal,
                           params.jethro_kerberos_keytab, params.jethro_user)

            self.ensure_instance_attached()

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

        # start metrics
        self.startMetrics()

    def stop(self, env):
        import params
        env.set_params(params)

        # stop metrics
        self.stopMetrics()

        Execute(
            ("service", "jethro", "stop", params.jethro_instance_name),
            user=params.jethro_user
        )

    def status(self, env):
        import status_params
        env.set_params(status_params)
        self.startMetrics()
        return check_process_status(status_params.jethroserver_pid_file)

    def configure(self, env):
        import params
        env.set_params(params)

    # ************************ Private methrods ***************************

    def ensure_instance_attached(self):
        import params
        create_attach_instance(
            self.JETHRO_SERVICE_NAME,
            params.jethro_instance_name,
            params.jethro_instance_storage_path,
            params.jethro_user
        )

    def startMetrics(self):
        jethro_metrice_collector = JethroMetrics()
        jethro_metrice_collector.submit_metrics()

    def stopMetrics(self):
        print("stopping jethro")


if __name__ == "__main__":
    JethroServer().execute()
