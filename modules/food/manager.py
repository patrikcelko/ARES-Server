############################
##      ARES Server       ##
##  Author: Patrik Čelko  ##
############################

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
        print(sub_route)
        return "Food manager"




