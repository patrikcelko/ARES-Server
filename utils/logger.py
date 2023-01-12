############################
##      ARES Server       ##
##  Author: Patrik Čelko  ##
############################

import logging
from configs import config
from flask.logging import default_handler


class AresLogger(logging.Logger):
    '''
    Custom server logger
    '''

    FORMATTER = '[%(asctime)s] [%(levelname)s]{}: %(message)s'
    
    def __init__(self, name: str, manager_name: str='') -> None:
        super().__init__(name, 
            logging.DEBUG if config.ALLOW_DEBUG else logging.INFO)
        self.addHandler(default_handler)
        default_handler.setFormatter(logging.Formatter(self.FORMATTER.format(manager_name)))

# Root logger
log: AresLogger = AresLogger(config.NAME)


