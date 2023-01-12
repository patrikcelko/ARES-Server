############################
##      ARES Server       ##
##  Author: Patrik Čelko  ##
############################

import logging
from configs import config

log = logging.getLogger(config.NAME)
log.setLevel(level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)