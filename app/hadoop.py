from app.webScrapping import web_scrapping
from tools.evironment import getHadoopConnectionInfo
from hdfs3 import HDFileSystem

class HadoopConnection:

    def __init__(self):
        host, port = getHadoopConnectionInfo()
        self.__hdfs = HDFileSystem(host= host, port= port)

    def getCOVIDData(self, version: int):
        print(self.__hdfs.cat('/minadzd/covid-' + str(version) + '.json'))

    def getFileCounter(self):
        return len(self.__hdfs.ls('/minadzd'))

    def putCOVIDData(self, data:str):
        version = self.getFileCounter()
        with self.__hdfs.open('/minadzd/covid-' + str(version) + '.json', 'wb') as f:
            f.write(b'%s' % data.encode('ascii'))

if __name__ == '__main__':
    hadoop = HadoopConnection()
    hadoop.putCOVIDData(web_scrapping())
    hadoop.getCOVIDData(1)