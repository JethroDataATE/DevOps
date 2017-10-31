import os
from resource_management.core import shell
from resource_management.libraries.functions.format import format

RESULT_STATE_OK = 'OK'
RESULT_STATE_CRITICAL = 'CRITICAL'
RESULT_STATE_WARNING = 'WARNING'
RESULT_STATE_UNKNOWN = 'UNKNOWN'
RESULT_STATE_SKIPPED = 'SKIPPED'

JETHRO_USER_KEY = '{{jethro-env/jethro_user}}'
JETHRO_PASS_KEY = '{{jethro-env/jethro_password}}'


def get_tokens():
    return (JETHRO_USER_KEY, JETHRO_PASS_KEY)


def load_src(name, fpath):
    import os
    import imp
    return imp.load_source(name, os.path.join(os.path.dirname(__file__), fpath))


def execute(configurations={}, parameters={}, host_name=None):

    load_src("jethro_service_utils", "../scripts/jethro_service_utils.py")
    import jethro_service_utils
    from jethro_service_utils import get_current_instance_name, get_current_instance_port

    jethro_user = configurations[JETHRO_USER_KEY]
    jethro_password = configurations[JETHRO_PASS_KEY]

    instance_name = get_current_instance_name()
    instance_port = get_current_instance_port()

    if instance_name is None:
        return RESULT_STATE_UNKNOWN, ['Unable to read Jethro auto-cube generation parameter because Jethro Server is unreachable.']

    client_code, client_out = shell.call(
        "service jethro status |  awk ' /" + instance_name + ".*JethroServer/ {x=$2} END{if(x != \"\") print x}'")
    if client_code != 0 or client_out.strip() == '':
        return RESULT_STATE_UNKNOWN, ['Unable to read Jethro auto-cube generation parameter becasue Jethro Server is unreachable.']

    cmd_part1 = format(
        "su - {jethro_user} -c \'JethroClient {instance_name} localhost:{instance_port} -u {jethro_user} -p {jethro_password} -q \"show param  dynamic.aggregation.auto.generate.enable;\"'")
    cmd_part2 = " | awk -F \"|\" '$4 ~ /dynamic.aggregation.auto.generate.enable/ {x=$5} END{print x}'"
    cmd = cmd_part1 + cmd_part2
    code, out = shell.call(cmd)
    if code == 0:
        res = out.strip()
        if res == '1':
            return RESULT_STATE_OK, [format("Jethro auto-cube generation is ON for instance '{instance_name}'.")]
        else:
            return RESULT_STATE_WARNING, [format("Jethro auto-cube generation is OFF for instance '{instance_name}'.")]
    else:
        return RESULT_STATE_UNKNOWN, ['Unable to read Jethro auto-cube generation parameter: ' + out]