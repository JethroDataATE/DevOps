#!/usr/bin/env python

from resource_management.core.source import StaticFile
from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import File, Execute
from resource_management.core.logger import Logger
from resource_management.libraries.functions.format import format
from jethro_metrics_utils import start_metrics
from jethro_service_utils import create_attach_instance, setup_kerberos, installJethroComponent, \
    ensure_kerberos_tickets, get_current_instance_name, \
    is_service_installed_for_instance, get_current_jethro_version
from resource_management.libraries.functions.check_process_status import check_process_status


class JethroLoadScheduler(Script):

    JETHRO_SERVICE_NAME = "loadscheduler"

    # ************************ Script Interface methrods ***************************

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)

        Logger.info("Install Jethro Load Scheduler")

        installJethroComponent(params.jethro_rpm_path, params.jethro_user)

        # if not params.security_enabled:
        #     self.ensure_instance_attached()

    def start(self, env):
        import params
        env.set_params(params)

        instance_name = get_current_instance_name()

        if params.security_enabled:
            setup_kerberos(params.kinit_path, params.jethro_kerberos_prinicipal,
                           params.jethro_kerberos_keytab, params.jethro_user)

        if instance_name is None:
            self.ensure_instance_attached()
            instance_name = get_current_instance_name()
        elif not is_service_installed_for_instance(instance_name, self.JETHRO_SERVICE_NAME):
            self.ensure_instance_attached()

        Execute(
            ("service", "jethro", "start",
             instance_name, self.JETHRO_SERVICE_NAME),
            user=params.jethro_user
        )

        self.configure(env)

        jethor_version = get_current_jethro_version(params.jethro_user)
        start_metrics(params.ams_collector_address, params.jethro_user, jethor_version)

    def stop(self, env):
        import params
        env.set_params(params)

        instance_name = get_current_instance_name()

        if instance_name is None:
            return

        Execute(
            ("service", "jethro", "stop",
             instance_name, self.JETHRO_SERVICE_NAME),
            user=params.jethro_user
        )

    def status(self, env):
        import status_params
        env.set_params(status_params)

        import params
        if params.security_enabled:
            ensure_kerberos_tickets(params.klist_path, params.kinit_path, params.jethro_kerberos_prinicipal,
                                    params.jethro_kerberos_keytab, params.jethro_user)

        if status_params.jethroloadschedule_pid_file is not None:
            return check_process_status(status_params.jethroloadschedule_pid_file)
        else:
            return check_process_status('')


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
            params.jethro_instance_cache_path,
            params.jethro_instance_cache_size,
            params.jethro_user
        )


if __name__ == "__main__":
    JethroLoadScheduler().execute()
