
############################
##      ARES Server       ##
##  Author: Patrik Čelko  ##
############################

from typing import List

from flask import Flask, Response
from exceptions.modul_errors import ModuleError
from exceptions.modul_errors import MissingManagerClassComponent
from utils.logger import AresLogger
from configs import config

class BaseManager:
    '''
    Base class for all modules managers

    Note: 
        - Manager class name must end with the word "Manager"
        - Manager must have filled all attributes mentioned in REQUIRED_ATTRIBUTES
    '''

    REQUIRED_ATTRIBUTES: List[str] = [
        "DESCRIPTION",
        "MANAGER_NAME",
    ]

    DESCRIPTION: str = None
    MANAGER_NAME: str = None

    def __init__(self, app: Flask) -> None:
        if app is None:
            raise ModuleError('The manager received an invalid instance of the Flask app.')
        self.app: Flask = app

        # Check if all required attributes were filled in children's classes
        for item in self.REQUIRED_ATTRIBUTES:
            if not getattr(self, item):
                raise MissingManagerClassComponent(f'The module must have a filled {item}.')

        self.log = AresLogger(config.NAME, self.MANAGER_NAME)

    def route(self, sub_route: List[str]) -> Response:
        raise NotImplemented('Missing implementation for the selected route.')
