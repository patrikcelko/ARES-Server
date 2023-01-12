############################
##      ARES Server       ##
##  Author: Patrik Čelko  ##
############################

import logging

from typing import Dict
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
   
    def format(self, record: logging.LogRecord):
        original_logger = self.FORMATS.get(record.levelno)
        return logging.Formatter(original_logger, 
            '[%d.%m.%Y %H:%M:%S]').format(record)


class AresLogger(logging.Logger):
    '''
    Custom server logger
    '''

    FORMATTER = '%(asctime)s %(levelname)-8s %(name)s%(message)s'
    
    def __init__(self, name: str, manager_name: str='', skip_adding=False) -> None:
        
        # Initialise formatter
        res_name = f'[{name}]{Color.RESET}: ' if not manager_name else \
            f'[{name}]-{Color.ORANGE}-[{manager_name}]{Color.RESET}: '
        super().__init__(res_name, logging.DEBUG if config.ALLOW_DEBUG else logging.INFO)
        self.ares_formatter = AresFormatter(self.FORMATTER)
        
        # Colors
        self.colorHandler = logging.StreamHandler()
        self.addHandler(self.colorHandler)
        self.colorHandler.setFormatter(AresFormatter(self.FORMATTER))


# Root logger (use only for system stuff)
log: AresLogger = AresLogger(config.NAME)
default_handler.setFormatter(log.ares_formatter)




