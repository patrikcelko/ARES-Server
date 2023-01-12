from modules.food.scrapers.base_scraper import BaseScraper

class NamaskarScraper(BaseScraper):

    SCRAPER_NAME = "namaskar.cz"

    def __init__(self):
        super().__init__()