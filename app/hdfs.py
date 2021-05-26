from tools.logger import Logger
from app.webScrapping import web_scrapping
from tools.evironment import get_HDFS_connection_info
from hdfs3 import HDFileSystem


class HDFSConnector:

    def __init__(self):
        self.logger = Logger('HDFS Connector')
        host, port = get_HDFS_connection_info()
        self.__hdfs = HDFileSystem(host = host, port = port)

    def get_covid_data(self, version: int) -> None:
        self.logger.log_entry('Get data from covid-%d.json file' % version)
        print(self.__hdfs.cat('/minadzd/covid-' + str(version) + '.json'))

    def get_covid_file_counter(self) -> None:
        return len(self.__hdfs.ls('/minadzd'))
    
    def clean_covid_data(self) -> None:
        if self.__hdfs.isdir('/minadzd'):
            self.logger.log_entry('Removed: ' + str(self.__hdfs.ls('/minadzd')))
            self.__hdfs.rm('/minadzd')
        else:
            self.logger.log_entry('Folder doesn\'t exist!', 'warn')
        self.__hdfs.mkdir('/minadzd')

    def put_covid_data(self, data) -> None:
        version = self.get_covid_file_counter()
        self.logger.log_entry('Recently covid data file: %s' % str(version + 1))

        with self.__hdfs.open('/minadzd/covid-' + str(version) + '.json', 'wb') as f:
            self.logger.log_entry('Putting data to hdfs')
            f.write(b'%s' % data.encode('ascii'))
            self.logger.log_entry('Putted data', 'debug')