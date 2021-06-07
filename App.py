# Imports
from tools.plotter import draw_plots
from app.docker import add_files_to_namenode, execute_mapreduce
from tools.logger import Logger
from app.webScrapping import web_scrapping
from tools.evironment import get_cloud_database_connection_string
from tools.intervalExecution import interval_refresh
from app.mongo import MongoDbDriver
from app.hdfs import HDFSConnector
from datetime import datetime


# Initialization
hdfs = HDFSConnector()
logger = Logger('App')

# Add mapper and reducer to docker image
add_files_to_namenode()

# Ask about interval download 
intervalGet = input('Czy dane mają być pobierane okresowo?([T]/n) ')
if intervalGet in ['T','t','Y','y', '']:
    interval = input('Co ile sekund (min. 60s) ma pobierac dane?[60] ')

    try:
        if interval != '' and float(interval) >= 60:
            interval_refresh(float(interval))

        else:
            if float(interval) < 60:
                print('Interval musi byc wiekszy niz 60s')
                logger.log_entry('Interval must be higher than 60 sec', 'warn')

            interval_refresh()
            
    except ValueError:
        if interval == '':
            print('Wprowadzony interval musi byc floatem! Uruchamiam interval defaultowy')
            logger.log_entry('Inputed interval must be float! Dispatch default interval', 'warn')
        interval_refresh()

else:
    covid_timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    mongo = MongoDbDriver(get_cloud_database_connection_string(), 'covidData', 'covid-data-%s' % covid_timestamp)
    hdfs.put_covid_data(web_scrapping())
    execute_mapreduce()
    covid_results = hdfs.get_result()
    mongo.put_data_to_db(covid_results)
    covid_results = hdfs.get_result()
    draw_plots(covid_results)
