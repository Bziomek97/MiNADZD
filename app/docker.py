import os
import docker

def get_namenode_container():
    return docker.from_env().containers.get('namenode')

def add_files_to_namenode():
    os.system('docker cp mapreduce/mapper.py namenode:mapper.py')
    os.system('docker cp mapreduce/reducer.py namenode:reducer.py')
    os.system('docker cp mapreduce/mapred.sh namenode:mapred.sh')
    get_namenode_container().exec_run('chmod +x mapred.sh')

def execute_mapreduce():
    get_namenode_container().exec_run('./mapred.sh')