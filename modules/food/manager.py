from modules.base_manager import BaseManager
from modules.food.scraper_manager import ScraperManager

class FoodManager(BaseManager):
    
    DESCRIPTION = 'Manager'
    MANAGER_NAME = 'Food'

    def __init__(self, app):
        super().__init__(app)
        self._scraper_manager: ScraperManager = ScraperManager()
        self.log.warn("A ja by som mal byt food")

    def route(self, sub_route):
        self.log.critical(self._scraper_manager._scrapers)
        scrap = self._scraper_manager._scrapers['namaskar.cz']
        self.log.critical(scrap)


        return scrap.run_scraper()
        #return "Food manager"




