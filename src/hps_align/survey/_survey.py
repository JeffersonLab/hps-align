
from ._utils import *
from ._uchannel import UChannel
from ._sensors import *
from ._cli import app


class Survey:

    def __init__(self):
        self.uchannel = UChannel()
        self.sensors = {'top': {}, 'bottom': {}}  # {volume: {layer: {sensor (ax/st): Sensor()}}}

    def set_uchannel(self, uchannel):
        self.uchannel = uchannel

    def set_sensors(self, sensors):
        self.sensors = sensors

    def get_pin_in_uchannel_ballframe(self, volume, layer):
        return self.uchannel.pin_in_ballframe(int(layer), volume)

    def transform_sensor_to_uchannel_ballframe(self, volume, layer, sensor_type):
        basis, origin = self.get_pin_in_uchannel_ballframe(volume, layer)
        sensor = self.sensors[volume][layer][sensor_type]

        sensor_origin_pin = sensor.get_sensor_origin_pinframe()
        sensor_normal_pin = sensor.get_sensor_normal_pinframe()

        sensor_origin_ball = origin + np.matmul(sensor_origin_pin, basis)
        sensor_normal_ball = np.matmul(sensor_normal_pin, basis)

        return sensor_origin_ball, sensor_normal_ball
