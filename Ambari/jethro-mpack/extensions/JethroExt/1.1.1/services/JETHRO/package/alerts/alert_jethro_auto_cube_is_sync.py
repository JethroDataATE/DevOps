from resource_management.core import shell
from resource_management.libraries.functions.format import format

RESULT_STATE_OK = 'OK'
RESULT_STATE_CRITICAL = 'CRITICAL'
RESULT_STATE_WARNING = 'WARNING'
RESULT_STATE_UNKNOWN = 'UNKNOWN'
RESULT_STATE_SKIPPED = 'SKIPPED'

JETHRO_USER_KEY = '{{jethro-env/jethro_user}}'
JETHRO_PASS_KEY = '{{jethro-env/jethro_password}}'
CUBE_GENERATION_FLAG = '{{jethro-global/dynamic.aggregation.auto.generate.enable}}'


def get_tokens():
    return (JETHRO_USER_KEY, JETHRO_PASS_KEY, CUBE_GENERATION_FLAG)


def load_src(name, fpath):
    import os
    import imp
    return imp.load_source(name, os.path.join(os.path.dirname(__file__), fpath))


def execute(configurations={}, parameters={}, host_name=None):

    try:
        load_src("jethro_service_utils", "../scripts/jethro_service_utils.py")
        import jethro_service_utils
        from jethro_service_utils import get_current_instance_name, get_current_instance_port

        jethro_user = configurations[JETHRO_USER_KEY]
        jethro_password = configurations[JETHRO_PASS_KEY]

        ambari_jethro_cube_param_bool_value = str(configurations[CUBE_GENERATION_FLAG])
        if ambari_jethro_cube_param_bool_value == 'true':
            ambari_jethro_cube_param_value = '1'
        else:
            ambari_jethro_cube_param_value = '0'

        instance_name = get_current_instance_name()
        instance_port = get_current_instance_port()

        if instance_name is None:
            return RESULT_STATE_UNKNOWN, ['Unable to read Jethro auto-cube generation parameter - Jethro Server is not reachable.']

        jethro_status_cmd =  "service jethro status | awk ' /JethroServer .*" + instance_name + "/ {x=$5} END{if(x != \"\") print x}'"

        client_code, client_out = shell.call(jethro_status_cmd, timeout=60)

        if client_code != 0 or client_out.strip() == '':
            return RESULT_STATE_UNKNOWN, ['Unable to read Jethro auto-cube generation parameter - Jethro Server is not reachable.']

        cmd_part1 = format("su - {jethro_user} -c \'JethroClient {instance_name} localhost:{instance_port} -u jethro -p {jethro_password} -q \"show param  dynamic.aggregation.auto.generate.enable;\"'")
        cmd_part2 = " | awk -F \"|\" '$4 ~ /dynamic.aggregation.auto.generate.enable/ {x=$5} END{print x}'"
        cmd = cmd_part1 + cmd_part2
        code, out=shell.call(cmd, timeout=60)
        if code == 0:
            res = out.strip()
            if res == ambari_jethro_cube_param_value:
                return RESULT_STATE_OK, [format("Jethro auto-cube generation parameter value is aligned with Ambari configuration for instance '{instance_name}'.")]
            else:
                return RESULT_STATE_WARNING, [format("Jethro auto-cube generation parameter value is stale for instance '{instance_name}'.\nAmbari configuration value is: {ambari_jethro_cube_param_value}, while Jethro actual value is {res}.")]
        else:
            return RESULT_STATE_UNKNOWN, ['Unable to read Jethro auto-cube generation parameter: ' + out]
    except Exception as e:
        return RESULT_STATE_UNKNOWN, ['Unable to read Jethro auto-cube generation parameter: ' + str(e)]
