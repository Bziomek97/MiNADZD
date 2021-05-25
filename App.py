# Imports
from app.mongo import MongoDbDriver
from app.hadoop import HadoopConnection
from tools.intervalExecution import intervalRefresh

# Initialization
hadoop = HadoopConnection()
mongo = MongoDbDriver()

intervalRefresh()