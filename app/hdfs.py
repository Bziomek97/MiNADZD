from tools.logger import Logger
from tools.evironment import get_HDFS_connection_info
from hdfs3 import HDFileSystem
import os
import json


class HDFSConnector:

    def __init__(self):
        self.logger = Logger('HDFS Connector')
        host, port = get_HDFS_connection_info()
        self.__hdfs = HDFileSystem(host = host, port = port)

    def get_covid_data(self, version: int) -> None:
        self.logger.log_entry('Get data from covid.json file')
        print(self.__hdfs.cat('/minadzd/covid.json'))

    def put_covid_data(self, data) -> None:
        if not self.__hdfs.isdir('/minadzd'):
            self.__hdfs.mkdir('/minadzd')
        
        with self.__hdfs.open('/minadzd/covid.json', 'wb') as f:
            self.logger.log_entry('Putting data to hdfs')
            f.write(b'%s' % data.encode('ascii'))
            self.logger.log_entry('Putted data', 'debug')
            
    def get_result(self):
        self.__hdfs.get('/results/part-00000','./results')

        file_lines = list()
        with open('./results') as f:
            file_lines = f.readlines()

        os.remove('./results')

        results_to_plot = dict()
        for line in file_lines:
            tmp = line.split('\t')

            results_to_plot[tmp[0]] = json.loads(tmp[1])

        return results_to_plot
        