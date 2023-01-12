
############################
##      ARES Server       ##
##  Author: Patrik Čelko  ##
############################

from modules.base_manager import BaseManager
from os import path
from typing import Callable, Dict, List
from exceptions.modul_errors import MissingManagerClass, MissingManagerClassComponent
from utils.logger import log
from os import listdir, path
from flask import Flask
from configs import config


class Utility:
    '''
    Utility class containing all necessary static methods for a smooth run :)
    '''
    
    @staticmethod
    def create_module_link(modules: Dict[str, BaseManager], address: str) -> Dict[str, str]:
        '''
        Static method that generates a dictionary containing descriptions of
        the API modules, based on loaded managers
        '''

        result_dict: Dict[str, str] = {}
        ssl_rep: str = 'https' if config.ALLOW_SSL else 'http'

        for name, module in modules.items():
            result_dict[name] = {
                'manager': module.MANAGER_NAME,
                'description': module.DESCRIPTION,
                'address': f'{ssl_rep}://{address}/{name}'
            }
        return result_dict

    @staticmethod
    def for_dict(fun: Callable, items: dict) -> None:
        '''
        Pseudo 'functional' alternative map over the dictionary without returning a result
        '''

        for key, val in items.items():
            fun(key, val)

    @staticmethod
    def rename_function(new_name: str) -> Callable:
        '''
        The static method that can as decorator during initialization change function name
        '''

        def decorator(fun: Callable) -> Callable:
            fun.__name__ = new_name
            return fun

        return decorator

    @staticmethod
    def route_wrapper(route_name: str, manager: BaseManager, app: Flask) -> Callable:
        '''
        The static method that will generate routes for all modules based on
        the folders in which they are located. We also support sub-routes, so
        we need to register them too.

        Internally this method wraps the method with a route decorator and maps
        received requests to the respective manager method "route". 
        '''

        log.debug(f'Decorating endpoint for module {route_name}')
        
        @app.route(str(f'/{route_name}/<path:sub_route>'))
        @Utility.rename_function(str(f'router_{route_name}'))
        def route_getter(sub_route: str):
            return manager.route(sub_route.split('/'))

        @app.route(str(f'/{route_name}/'))
        @Utility.rename_function(str(f'main_router_{route_name}'))
        def route_getter():
            return manager.route(None)
        
        return route_getter

    @staticmethod
    def proccess_imports(import_obj, name: str) -> Dict[str, BaseManager]:
        '''
        The static method that will based on the import object retrieve 
        manager class specific for the module name
        '''

        tmp_import = getattr(getattr(import_obj, name), 'manager')
        avalible_atributes: List[str] = dir(tmp_import)

        for attribute in avalible_atributes:
            if not attribute.endswith('Manager') or attribute == 'BaseManager':
                continue  # Get rid of none-Manager classes

            candidate_class = getattr(tmp_import, attribute)
            if not issubclass(candidate_class, BaseManager):
                continue
            
            class_attributes: List[str] = dir(getattr(tmp_import, attribute))
            for attribute in BaseManager.REQUIRED_ATTRIBUTES:
                if attribute not in class_attributes:
                    raise MissingManagerClassComponent(\
                        f'Was not able to locate attribute {attribute} in manager for module {name}.')
            
            log.debug(f'Successfully loaded {name}.')
            return (name, candidate_class)
    
        raise MissingManagerClass(f'Was not able to load manager for module {name}.')

    @staticmethod
    def get_managers_name(main_path: str) -> List[str]:
        '''
            The static function that automatically goes through all folders in 
            the folder "modules" and returns all manager's names that will be 
            able to find as list
        '''

        modules_path: str  = f'{path.dirname(path.abspath(main_path))}/modules/'
        module_names: List[str] = list(filter(
            lambda val: not val.startswith('__') and '.' not in val and \
                path.isdir(f'{modules_path}{val}'), 
            listdir(modules_path))
        )
        module_size: int = len(module_names)

        if module_size <= 0:
            log.warning('Something is possibly wrong, mo manger was found.')
            return module_names  # This will be for sure [ ]

        log.info(f'Successfully found {module_size}.')
        log.debug(f'Found modules: {module_names}')

        return module_names
