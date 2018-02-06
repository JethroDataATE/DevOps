from resource_management.libraries.functions.format import format
from resource_management.core import shell

RESULT_STATE_OK = 'OK'
RESULT_STATE_CRITICAL = 'CRITICAL'
RESULT_STATE_WARNING = 'WARNING'
RESULT_STATE_UNKNOWN = 'UNKNOWN'
RESULT_STATE_SKIPPED = 'SKIPPED'

JETHRO_USER_KEY = '{{jethro-env/jethro_user}}'

def get_tokens():
    return (JETHRO_USER_KEY, )

def execute(configurations={}, parameters={}, host_name=None):
    try:
        jethro_user = configurations[JETHRO_USER_KEY]
        
        monitor_status_cmd = format("su - {jethro_user} -c 'service jethro status'") + " | awk '{if ($2 == \"JethroMonitor\") print $2}'"
        client_code, client_out = shell.call(monitor_status_cmd, timeout=60)

        if client_code == 0 and client_out.strip() == 'JethroMonitor':
            return RESULT_STATE_OK, ["Jethro Monitor is up and running."]
        else:
            return RESULT_STATE_CRITICAL, ["Jethro Monitor is down."]
    except Exception as e:
        strErr = str(e)
        return RESULT_STATE_UNKNOWN, [format('Unable to determine whether Jethro Monitor is running: {strErr}.')]

