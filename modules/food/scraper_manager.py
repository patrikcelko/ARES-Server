from typing import Dict, List, Optional, Set
from modules.food.scrapers.base_scraper import BaseScraper
from modules.food.scrapers import *
from exceptions.scraper_errors import ScraperLoadingError, MissingScraperClass
import sys
from utils.logger import log

# This might looks wierd, but we need to retrieve data from module, in class it will not work
RAW_DIRS: list = dir()

class ScraperManager():

    def __init__(self) -> None:
        self._raw_dirs: List[str] = RAW_DIRS
        self._scrapers: Dict[str, BaseScraper] = { }
        
        try:
            self._init_scrapers()
        except Exception as exc:
            if isinstance(exc, ScraperLoadingError):
                raise  # Reraise same custom exception
            raise ScraperLoadingError(f'Was not able to load one of the scrapers. Original message: {exc}') 


    def _init_scrapers(self):
        '''
            Simple "private" method that will initialise all avalible scrapers in scrapers dict
        '''

        for scraper_name in self._raw_dirs:
            split_raw = scraper_name.split('_')
            if split_raw[-1] != 'scraper':
                continue

            module_base: str = f'modules.food.scrapers.{scraper_name}'
            temp_attributes: List[BaseScraper] = dir(sys.modules[module_base])
            class_candidates: Set[str] = set()
            
            for module_attribte in temp_attributes:
                if module_attribte.endswith('Scraper') and module_attribte != 'BaseScraper':
                    class_candidates.add(module_attribte)
            
            if len(class_candidates) != 1:
                raise MissingScraperClass(f'Invalid amount of scraper candidates ({len(class_candidates)}).')
            
            class_name: str = class_candidates.pop()
            scraper_class = getattr(sys.modules[module_base], class_name)
            if not issubclass(scraper_class, BaseScraper):
                raise MissingScraperClass(f'Loaded class is not derived from BaseScraper. Class name: {class_name}.')
            
            scraper_instance: BaseScraper = scraper_class()  # Initialise scraper
            if scraper_instance.SCRAPER_NAME in self._scrapers:
                continue  # If scraer is already loaded just skip
            self._scrapers[scraper_instance.SCRAPER_NAME] = scraper_instance

    def get_names(self) -> Set[str]:
        '''
            Method that will return set of all avalible scrapers names
        '''
        return set(self._scrapers.keys)

    def get_scraper(self, name) -> BaseScraper:
        '''
            Method that will return instance of the scraper based on the name. If name is invalid
            exception will be raised.
        '''
        scraper_instance: Optional[BaseScraper] = self._scrapers.get(name)
        if scraper_instance is not None:
            return scraper_instance
        raise MissingScraperClass(f'Was not able to find scraper: {name}')

    def run_all(self):
        '''
            Run all avalible scrapers
        '''
        for scraper_name, scraper_instance in self._scrapers.items():
            scraper_instance.run_scraper()