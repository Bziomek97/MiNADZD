from tools.evironment import getDatabaseConnectionPath
import pymongo

class MongoDbDriver:

    def __init__(self):
        self.__client = pymongo.MongoClient(getDatabaseConnectionPath(), tls=True)

    def test(self):
        print(self.__client.test)

if __name__ == '__main__':
    mongo = MongoDbDriver()
    mongo.test()