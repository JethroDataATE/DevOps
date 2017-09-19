#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.libraries.functions.check_process_status import check_process_status


class ServiceCheck(Script):
    def service_check(self, env):
        return 1


if __name__ == "__main__":
    ServiceCheck().execute()
