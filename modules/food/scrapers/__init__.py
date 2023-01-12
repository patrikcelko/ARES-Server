from typing import List
from os import listdir, path
from utils.logger import log

def _get_avalible_scrapers(scrapers_path: str) -> List[str]:
    avalible_modules: List[str] = listdir(path.dirname(path.abspath(scrapers_path)))
    res_modules: List[str] = []

    for temp_module in avalible_modules:
        if not temp_module.endswith('scraper.py') or temp_module.endswith('base_scraper.py'):
            continue
        if '.' in temp_module:  # Prevent problems with none .py files
            res_modules.append(temp_module.split('.')[0])
            continue
        log.debug(f'Found scraper without .py postfix, value: {temp_module}')
    
    log.info(f'Successfully loaded {len(res_modules)} scraping modules.')
    log.debug(f'Loaded scraping modules: {res_modules}')
    return res_modules

__all__ = _get_avalible_scrapers(__file__)