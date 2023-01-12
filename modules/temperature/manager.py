
############################
##      ARES Server       ##
##  Author: Patrik Čelko  ##
############################

from psutil import sensors_temperatures
from exceptions.temp_sensor_errors import NoTempSensors
from modules.base_manager import BaseManager

class TemperatureManager(BaseManager):

    DESCRIPTION = "Display actual temperatures."
    MANAGER_NAME = "Temperature"

    # Sensors that we are looking for
    SENSOR_NAMES = [
        'nvme',
        'coretemp',
    ]

    def route(self, sub_route):
        return "Temperature manager"

    def __init__(self, app):
        super().__init__(app)
        
        self.data = []

    def _scrape_data(self):
        # We need to reset previously saved data
        self.data = []

        raw_data = sensors_temperatures()
        for to_find in self.SENSOR_NAMES:
            if to_find not in raw_data:
                raise NoTempSensors(to_find)
            for node in raw_data[to_find]:
                # [0] - Name, [1] - Actual temperature
                self.data.append({
                    "node-name": node[0],
                    "temperature": node[1]
                })

    def to_json(self):
        self._scrape_data()
        return self.data