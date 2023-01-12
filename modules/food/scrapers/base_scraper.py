############################
##      ARES Server       ##
##  Author: Patrik Čelko  ##
############################

from datetime import datetime
from configs import config

'''
Basic class for scrapers

Note: All scrapers classes must ends with word "Scraper"
'''
class BaseScraper():

    SCRAPER_NAME: str = None

    def __init__(self) -> None:
        self.last_run: datetime = None
        if self.SCRAPER_NAME is None:
            raise NotImplementedError('The scraper must have implemented the name.')

    def run_scraper(self) -> None:
        raise NotImplementedError(f'Run implementation for {self.SCRAPER_NAME}, does not exist.')

    def get_data(self) -> dict:
        raise NotImplementedError(f'Get data implementation for {self.SCRAPER_NAME}, does not exist.')
    
    def __str__(self) -> str:
        last_run_rep: str = 'NEVER' if self.last_run is None else self.last_run.strftime(config.TIME_FORMAT)
        return f'[{self.SCRAPER_NAME}]: Last run: {last_run_rep}'
