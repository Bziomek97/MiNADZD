from app.webScrapping import web_scrapping
from app.hdfs import HDFSConnector
from tools.logger import Logger
import threading


def interval_refresh(interval: float = 180.0) -> None:
    threading.Timer(interval, interval_refresh).start()

    logger = Logger('Interval data refresh')

    logger.log_entry('Dispatch interval task')
    hadoopConnection = HDFSConnector()
    hadoopConnection.put_covid_data(web_scrapping())

    logger.log_entry('Clean up after download', 'debug')
    del hadoopConnection, logger