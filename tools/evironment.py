from pyaml_env import parse_config

variable_file = './var/env.yaml'
config = parse_config(variable_file)

def getDatabaseConnectionPath():
    return config['DATABASE']

def getDebugInfo() -> str:
    return config['DEBUG']

def getHadoopConnectionInfo():
    host = config['HDFS']['host']
    port = config['HDFS']['port']
    return host, port