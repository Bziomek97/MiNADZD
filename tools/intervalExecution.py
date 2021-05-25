from app.webScrapping import web_scrapping
from app.hadoop import HadoopConnection
import threading

def intervalRefresh():
    threading.Timer(180.0, intervalRefresh).start()
    hadoopConnection = HadoopConnection()
    hadoopConnection.putCOVIDData(web_scrapping())
    del hadoopConnection