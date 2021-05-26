# Imports
from tools.logger import Logger
from app.webScrapping import web_scrapping
from tools.evironment import get_cloud_database_connection_string
from tools.intervalExecution import interval_refresh
from app.mongo import MongoDbDriver
from app.hdfs import HDFSConnector


# Initialization
hadoop = HDFSConnector()
mongo = MongoDbDriver(get_cloud_database_connection_string(), 'covidData', 'test')
logger = Logger('App')

# Ask about clean data in HDFS
clean = input('Czy dane mają być wyczyszczone?([T]/n) ')
if clean in ['T','t','Y','y', '']:
    logger.log_entry('Dane zostana wyczyszczone')
    hadoop.clean_covid_data()
    logger.log_entry('Dane zostaly wyczyszczone')
else:
    logger.log_entry('Dane nie zostaly wyczyszczone')

# Ask about interval download 
intervalGet = input('Czy dane mają być pobierane okresowo?([T]/n) ')
if intervalGet in ['T','t','Y','y', '']:
    interval = input('Co ile sekund (min. 180s) ma pobierac dane?[180] ')

    try:
        if interval != '' and float(interval) >= 180:
            interval_refresh(float(interval))

        else:
            if float(interval) < 180:
                print('Interval musi byc wiekszy niz 180s')
                logger.log_entry('Interval must be higher than 180 sec', 'warn')

            interval_refresh()
            
    except ValueError:
        print('Wprowadzony interval musi byc floatem! Uruchamiam interval defaultowy')
        logger.log_entry('Inputed interval must be float! Dispatch default interval', 'warn')
        interval_refresh()

else:
    hadoop.put_covid_data(web_scrapping())
