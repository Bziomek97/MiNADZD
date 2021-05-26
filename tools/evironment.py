import typing
from pyaml_env import parse_config


variable_file = './var/env.yaml'
config = parse_config(variable_file)

def get_cloud_database_connection_string() -> str:
    return config['DATABASE']

def get_debug_info() -> str:
    return config['DEBUG']

def get_HDFS_connection_info() -> typing.Tuple[str, str]:
    host = config['HDFS']['host']
    port = config['HDFS']['port']
    return host, port

def get_local_database_connection_string() -> str:
    return config['LOCAL_DATABASE']