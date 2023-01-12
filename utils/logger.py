############################
##      ARES Server       ##
##  Author: Patrik Čelko  ##
############################

from typing import Dict
import logging
from configs import config
from flask.logging import default_handler
from configs.colors import Color


class AresFormatter(logging.Formatter):
    '''
    Class representing colored formatter
    '''

    LEVEL_COLORS: Dict[int, str] = {
        logging.DEBUG: Color.GREY,
        logging.INFO: Color.BLUE,
        logging.WARNING: Color.YELLOW,
        logging.ERROR: Color.RED,
        logging.CRITICAL: Color.BLOD_RED
    }

    def __init__(self, formatter):
        super().__init__(formatter)
        self.formatter = formatter

        self.FORMATS: Dict[str, str] = dict(list(map(
            lambda val: (val[0], f'{val[1]}{self.formatter}{Color.RESET}'), 
            self.LEVEL_COLORS.items()
        )))
   
    def format(self, record):
        original_logger = self.FORMATS.get(record.levelno)
        return logging.Formatter(original_logger).format(record)


class AresLogger(logging.Logger):
    '''
    Custom server logger
    '''

    FORMATTER = '[%(asctime)s] [%(levelname)s]{}: %(message)s'
    
    def __init__(self, name: str, manager_name: str='') -> None:
        super().__init__(name, 
            logging.DEBUG if config.ALLOW_DEBUG else logging.INFO)
        self.addHandler(default_handler)
        default_handler.setFormatter(AresFormatter(self.FORMATTER.format(manager_name)))

# Root logger
log: AresLogger = AresLogger(config.NAME)




