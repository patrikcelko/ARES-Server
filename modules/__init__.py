############################
##      ARES Server       ##
##  Author: Patrik Čelko  ##
############################

from typing import List
from os import listdir, path
from utils.logger import log

def _get_modules(mod_path: str) -> List[str]:
    '''
    The function that retrieves all available modules in the modules folder
    '''

    modules_path: str = f'{path.dirname(path.abspath(mod_path))}/'
    modules: List[str] = list(filter(
        lambda val: not val.startswith('__') and '.' not in val and path.isdir(f'{modules_path}{val}'), 
        listdir(modules_path))
    )
    
    log.debug(f'Detected {len(modules)}, listed: {modules}.')
    return modules

__all__ = _get_modules(__file__)