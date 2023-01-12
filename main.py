############################
##      ARES Server       ##
##  Author: Patrik Čelko  ##
############################

import logging

from typing import Dict
from flask import Flask
from utils.utility import Utility
from modules.base_manager import BaseManager
from utils.logger import AresLogger

from configs import config

'''
ARES Server entry point.

application -> Flask app instance
modules -> List of the modules
'''

# Initialise logger
logging.setLoggerClass(AresLogger)

# Main application instance
application: Flask = Flask(config.NAME)

# Initialise managers (modules)
modules: Dict[str, BaseManager] = \
    dict(map(lambda man_tuple : (man_tuple[0], man_tuple[1](application)), 
    map(lambda val: Utility.proccess_imports(__import__(f'modules.{val}.manager'), val), 
        Utility.get_managers_name(__file__))))

# Initialise routes
Utility.for_dict(lambda key, val: Utility.route_wrapper(key, val, application), modules)

# Default info route
@application.route('/')
def get_info():
    return {
        'name': config.NAME,
        'address': config.ADDRESS,
        'version': config.VERSION,
        'author': 'Patrik Čelko',  # Hell yeah, fixed value :D
        'avalible-modules': 
            Utility.create_module_link(modules, config.ADDRESS)
    }

if __name__ == "__main__":
    application.run(
        ssl_context='adhoc', 
        threaded=True,
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        debug=config.ALLOW_DEBUG
    )