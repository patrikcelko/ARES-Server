
from modules.base_manager import BaseManager
from modules.food.scraper_manager import ScraperManager




class FoodManager(BaseManager):
    
    DESCRIPTION = 'API providing scrapings from restaurants'
    MANAGER_NAME = 'Food Manager'

    def __init__(self, app):
        super().__init__(app)
        self._scraper_manager: ScraperManager = ScraperManager()
        

    def test(self):
        return 'ahoj' 

    def route(self, sub_route):
        print(sub_route)
        return "Food manager"




