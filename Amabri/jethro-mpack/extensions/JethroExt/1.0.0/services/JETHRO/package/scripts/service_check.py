#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.libraries.functions.check_process_status import check_process_status


class ServiceCheck(Script):
    def service_check(self, env):
        import status_params
        env.set_params(status_params)
        return check_process_status(status_params.jethroserver_pid_file)


if __name__ == "__main__":
    ServiceCheck().execute()
