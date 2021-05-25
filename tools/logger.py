from tools.evironment import getDebugInfo
import time
import datetime

class Logger:
    debug_mode = getDebugInfo()

    def __init__(self, componentName: str) -> None:
        self.component = componentName

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

        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print("[%s][%s][%s] %s" % (st, self.component, level, message))