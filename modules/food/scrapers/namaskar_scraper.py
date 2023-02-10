from modules.food.scrapers.base_scraper import BaseScraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class NamaskarScraper(BaseScraper):

    SCRAPER_NAME = "namaskar.cz"
    URL = "namaskar.cz"

    def __init__(self):
        super().__init__()


    def run_scraper(self) -> None:
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox");
        chrome_options.add_argument("--disable-dev-shm-usage");
        chrome_options.headless = True # also works
        scraper = webdriver.Chrome(chrome_options=chrome_options, executable_path='/bin/chromedriver', service_log_path='/home/ares/ares/logs/ghostdriver.log')
        element = scraper.find_elements_by_xpath('/html')
        print(driver.page_source.encode("utf-8"))
        print(element)
        return str(element)
