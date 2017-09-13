#!/usr/bin/env python

import os

from resource_management.core.logger import Logger
from resource_management.core.resources.system import Execute
from resource_management.libraries.functions.format import format
from resource_management.libraries.script import Script

class ServiceCheck(Script):
    def service_check(self, env):
        import params
        env.set_params(params)
        Execute(
            ("service","jethro", "status"),
            user=params.jethro_user
        )

if __name__ == "__main__":
    ServiceCheck().execute()