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

    REWRITE_RULE = {
        'selenium.webdriver.remote.remote_connection': 'Selenium-Driver',
    }

    FORMATTER = '%(asctime)s %(levelname)-8s %(name)s%(message)s'
    
    def __init__(self, name: str, manager_name: str='', skip_adding=False) -> None:
        
        # Mekanism to override some badly composed names of loggers
        rewrite_value = self.REWRITE_RULE.get(name)
        if rewrite_value:
            name = rewrite_value

        # Initialise formatter
        res_name = f'[{name}]{Color.RESET}: ' if not manager_name else \
            f'[{name}]-{Color.ORANGE}-[{manager_name}]{Color.RESET}: '

        super().__init__(res_name, logging.DEBUG if config.ALLOW_DEBUG else logging.INFO)

        self.ares_formatter = AresFormatter(self.FORMATTER)
        
        # Colors
        self.colorHandler: logging.StreamHandler = logging.StreamHandler()
        self.addHandler(self.colorHandler)
        self.colorHandler.setFormatter(AresFormatter(self.FORMATTER))


# Root logger (use only for system stuff)
log: AresLogger = AresLogger(config.NAME)
default_handler.setFormatter(log.ares_formatter)




