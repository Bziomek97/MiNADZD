from app.mongo import MongoDbDriver
from tools.evironment import get_debug_info, get_local_database_connection_string
from datetime import datetime
import time


class Logger:
    debug_mode = get_debug_info()

    def __init__(self, componentName: str) -> None:
        self.component = componentName
        st = datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y_%Hh')
        self.__client = MongoDbDriver(get_local_database_connection_string(), 'minadzd', 'Logs-%s' % st)

    def log_entry(self, message: str, level: str = 'inf') -> None:
        '''Function to create and print logs
        
        Parameters: \n
        message - string with message \n
        level - info about type of log ['inf', 'warn', 'err', 'debug']. Default inf

        '''
        if not level in ['inf', 'warn', 'err', 'debug']:
            raise TypeError("Log's level doesnt fit to type. Instead of use one of this: ['inf', 'warn', 'err', 'debug']")
        elif self.debug_mode and level == 'debug':
            return

        if self.debug_mode and level == 'debug':
            st = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            print("[%s][%s][%s] %s" % (st, self.component, level, message))
            
        else:
            logData = {
                'loglevel': level,
                'component': self.component,
                'message': message,
                'timestamp': datetime.timestamp(datetime.now())
            }
            
            self.__client.put_data_to_db(logData)