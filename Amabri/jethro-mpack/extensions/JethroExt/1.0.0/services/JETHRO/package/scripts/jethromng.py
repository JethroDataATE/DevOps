#!/usr/bin/env python

from resource_management.core.source import StaticFile
from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import File, Execute
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.check_process_status import check_process_status
from jethro_service_utils import installJethroComponent
import os
import sys
import subprocess


class JethroMng(Script):

    # ************************ Script Interface methrods ***************************

    def install(self, env):
        import params
        env.set_params(params)
        print('Install Jethro Manager')
        installJethroComponent(params.jethromng_rpm_path, params.jethro_user)

    def start(self, env):
        import params
        env.set_params(params)
        print('Start the Jethro Manager')
        Execute(
            ("service", "jethromng", "start"),
            user=params.jethro_user
        )
        self.configure(env)

        # start metrics
        # self.startMetrics(params.ams_collector_address)
        
    def stop(self, env):
        import params
        env.set_params(params)
        print('Stop the Jethro Manager')
        Execute(
            ("service", "jethromng", "stop"),
            user=params.jethro_user
        )

        # stop metrics
        # self.stopMetrics()

    def status(self, env):
        import status_params
        env.set_params(status_params)

        print('Status of the Jethro Manager')
        return check_process_status(status_params.jethromng_pid_file)

    def configure(self, env):
        print('Configure the Jethro Manager')
        import params
        env.set_params(params)

    # ************************ Private methrods ***************************

    def startMetrics(self, ams_collector_address):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = format('{script_dir}/jethromng_metrics.py')
        subprocess.Popen(['python', script_path, ams_collector_address, ' &'])


    def stopMetrics(self):
        for line in os.popen("COLUMNS=20000 ps ax | grep jethromng_metrics | grep -v grep"):
            fields = line.split()
            pid = fields[0]
            os.kill(int(pid), 15)


if __name__ == "__main__":
    JethroMng().execute()
