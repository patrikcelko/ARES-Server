from enum import Enum

class Color(Enum):
    '''
    Enumeration of available colors used in terminal
    '''

    GREY = '\x1b[38;21m'
    BLUE = '\x1b[38;5;39m'
    YELLOW = '\x1b[38;5;226m'
    RED = '\x1b[38;5;196m'
    BLOD_RED = '\x1b[31;1m'
    RESET = '\x1b[0m'
    ORANGE = '\x1b[93m'

    def __str__(self):
        '''
        Ensure representation for function "str()"
        '''
        return str(self.value)