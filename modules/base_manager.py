
############################
##      ARES Server       ##
##  Author: Patrik Čelko  ##
############################

from typing import List

from flask import Flask
from exceptions.modul_errors import ModuleError

'''
    Base class for all modules managers

    Note: Manager class name must ends with wird "Manager"
'''
class BaseManager:

    DESCRIPTION: str = None
    MANAGER_NAME: str = None

    def __init__(self, app: Flask) -> None:
        if app is None:
            raise ModuleError('Manager recieved invalid instance of the Flask app.')
        self.app: Flask = app

        if self.DESCRIPTION is None or self.MANAGER_NAME is None:
            raise NotImplementedError('The module must have filled description and name.')

    def route(self, sub_route: List[str]):
        raise NotImplemented('Missing implementation for selected route.')

