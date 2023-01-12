
class NoTempSensors(Exception):
    def __init__(self, sensor_name: str):
        super().__init__(f'Was not able to read data from the sensor: {sensor_name}')
