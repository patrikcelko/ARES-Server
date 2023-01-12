
############################
##      ARES Server       ##
##  Author: Patrik Čelko  ##
############################

from multiprocessing.managers import BaseManager
from os import path
from typing import Dict
from exceptions.modul_errors import MissingManagerClass
from utils.logger import log
from os import listdir, path
from flask import Flask

from configs import config


class Utility:
    
    @staticmethod
    def create_module_link(modules: Dict[str, BaseManager], address: str):
        result_dict = {}
        for name, module in modules.items():
            ssl_rep = 'https' if config.ALLOW_SSL else 'http'
            result_dict[name] = {
                'manager': module.MANAGER_NAME,
                'description': module.DESCRIPTION,
                'address': f'{ssl_rep}://{address}/{name}'
            }
        return result_dict

    @staticmethod
    def for_dict(fun, items):
        for key, val in items.items():
            fun(key, val)

    @staticmethod
    def rename_function(new_name):
        def decorator(fun):
            fun.__name__ = new_name
            return fun

        return decorator

    @staticmethod
    def route_wrapper(route_name: str, manager: BaseManager, app: Flask):
        log.debug(f'Decorating endpoint for module {route_name}')
        
        @app.route(str(f'/{route_name}/<path:sub_route>'))
        @Utility.rename_function(str(f'router_{route_name}'))
        def route_getter(sub_route):
            return manager.route(sub_route.split('/'))

        @app.route(str(f'/{route_name}/'))
        @Utility.rename_function(str(f'main_router_{route_name}'))
        def route_getter():
            return manager.route(None)
        
        return route_getter

    @staticmethod
    def proccess_imports(import_obj, name):
        tmp_import = getattr(getattr(import_obj, name), 'manager')
        avalible_atributes = dir(tmp_import)

        for attribute in avalible_atributes:
            if not attribute.endswith('Manager') or attribute == 'BaseManager':
                continue
            candidate_class = getattr(tmp_import, attribute)
            if 'MANAGER_NAME' in dir(getattr(tmp_import, attribute)):
                return (name, candidate_class)
            log.debug(f'Successfully loaded {name}.')
    
        raise MissingManagerClass(f'Was not abel to load manager for module {name}.')

    @staticmethod
    def get_managers_name(main_path):
        '''
            Function that will automatically go throu all folders in folder modules and
            all managers names that will be able to found
        '''

        modules_path = f'{path.dirname(path.abspath(main_path))}/modules/'
        module_names = list(filter(
            lambda val: not val.startswith('__') and '.' not in val and path.isdir(f'{modules_path}{val}'), 
            listdir(modules_path))
        )
        log.info(f'Successfully found {len(module_names)}.')
        log.debug(f'Found modules: {module_names}')

        return module_names