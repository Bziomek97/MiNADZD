from app.mongo import MongoDbDriver
from tools.plotter import draw_plots
from app.docker import execute_mapreduce
from app.webScrapping import web_scrapping
from app.hdfs import HDFSConnector
from tools.logger import Logger
from datetime import datetime
from tools.evironment import get_cloud_database_connection_string
import threading


def interval_refresh(interval: float = 60.0) -> None:
    threading.Timer(interval, interval_refresh).start()
    covid_timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    mongo = MongoDbDriver(get_cloud_database_connection_string(), 'covidData', 'covid-data-%s' % covid_timestamp)

    logger = Logger('Interval data refresh')

    logger.log_entry('Dispatch interval task')
    hdfsConnection = HDFSConnector()
    hdfsConnection.put_covid_data(web_scrapping())
    execute_mapreduce()
    covid_results = hdfsConnection.get_result()
    mongo.put_data_to_db(covid_results)
    covid_results = hdfsConnection.get_result()
    draw_plots(covid_results)

    logger.log_entry('Clean up after download', 'debug')
    del hdfsConnection, logger, covid_results