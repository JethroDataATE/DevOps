#!/usr/bin/env python

from resource_management.core.source import StaticFile
from resource_management.libraries.script.script import Script
from resource_management.core.logger import Logger
from resource_management.core.resources.system import File, Execute
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.check_process_status import check_process_status
from jethro_service_utils import installJethroComponent

class JethroMng(Script):

    # ************************ Script Interface methrods ***************************

    def install(self, env):
        import params
        env.set_params(params)
        Logger.info('Install Jethro Manager')
        installJethroComponent(params.jethromng_rpm_path, params.jethro_user)

    def start(self, env):
        import params
        env.set_params(params)
        Logger.info('Start Jethro Manager')
        Execute(
            ("service", "jethromng", "start"),
            user=params.jethro_user
        )
        self.configure(env)

        
    def stop(self, env):
        import params
        env.set_params(params)
        Logger.info('Stop Jethro Manager')
        Execute(
            ("service", "jethromng", "stop"),
            user=params.jethro_user
        )

    def status(self, env):
        import mng_status_params
        env.set_params(mng_status_params)

        return check_process_status(mng_status_params.jethromng_pid_file)

    def configure(self, env):
        import params
        env.set_params(params)


if __name__ == "__main__":
    JethroMng().execute()
