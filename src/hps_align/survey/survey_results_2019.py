
from ._utils import *
from ._uchannel import UChannel
from ._ballframe import *
from ._pinframe import *
from ._sensors import *
from ._survey import Survey

from ._cli import app


class Survey2019(Survey):

    def __init__(self, survey_files):
        """Initialize Survey object with 2019 configuration"""

        ballframe_top = MattBallFrame(survey_files['ballframe_top'])
        ballframe_bottom = MattBallFrame(survey_files['ballframe_bottom'])
        pinframe_top = PinFrame(survey_files['pinframe_top'])
        pinframe_bottom = PinFrame(survey_files['pinframe_bottom'])

        self.uchannel = UChannel(ballframe_top=ballframe_top,
                                 ballframe_bot=ballframe_bottom,
                                 pinframe_top=pinframe_top,
                                 pinframe_bot=pinframe_bottom)

        matt_fixture = MattFixture(survey_files['matt_fixture'])
        sho_fixture = ShoFixture(survey_files['sho_fixture'])

        L0_axial_top = MattSensor(matt_fixture, survey_files['L0_axial_top'])
        L0_stereo_top = MattSensor(matt_fixture, survey_files['L0_stereo_top'])
        L1_axial_top = MattSensor(sho_fixture, survey_files['L1_axial_top'])
        L1_stereo_top = MattSensor(sho_fixture, survey_files['L1_stereo_top'])

        L0_axial_bottom = MattSensor(matt_fixture, survey_files['L0_axial_bottom'])
        L0_stereo_bottom = MattSensor(matt_fixture, survey_files['L0_stereo_bottom'])
        L1_axial_bottom = MattSensor(sho_fixture, survey_files['L1_axial_bottom'])
        L1_stereo_bottom = MattSensor(sho_fixture, survey_files['L1_stereo_bottom'])

        self.sensors = {
            'top': {
                '0': {
                    'axial': L0_axial_top,
                    'stereo': L0_stereo_top
                },
                '1': {
                    'axial': L1_axial_top,
                    'stereo': L1_stereo_top
                }
            },
            'bottom': {
                '0': {
                    'axial': L0_axial_bottom,
                    'stereo': L0_stereo_bottom
                },
                '1': {
                    'axial': L1_axial_bottom,
                    'stereo': L1_stereo_bottom
                }
            }
        }

    def get_pin_in_uchannel_ballframe(self, volume, layer):
        return self.uchannel.pin_in_ballframe(int(layer), volume)

    def transform_sensor_to_uchannel_ballframe(self, volume, layer, sensor_type):
        basis, origin = self.get_pin_in_uchannel_ballframe(volume, layer)
        sensor = self.sensors[volume][layer][sensor_type]

        sensor_origin_pin = sensor.get_sensor_origin_pinframe()
        sensor_normal_pin = sensor.get_sensor_normal_pinframe()
        print('sensor_origin_pin ', sensor_origin_pin)

        sensor_origin_ball = origin + np.matmul(sensor_origin_pin, basis)
        sensor_normal_ball = np.matmul(sensor_normal_pin, basis)

        return sensor_origin_ball, sensor_normal_ball
    
    def print_results(self, out_name):
        """Print results to file"""
        with open(out_name, 'w') as f:
            f.write('volume layer sensor_type x y z nx ny nz\n')
            for volume in ['top', 'bottom']:
                for layer in ['0', '1']:
                    for sensor_type in ['axial', 'stereo']:
                        sensor_origin_ball, sensor_normal_ball = self.transform_sensor_to_uchannel_ballframe(volume, layer, sensor_type)
                        f.write('{} {} {} {} {} {} {} {} {}\n'.format(volume, layer, sensor_type, sensor_origin_ball[0], sensor_origin_ball[1], sensor_origin_ball[2], sensor_normal_ball[0], sensor_normal_ball[1], sensor_normal_ball[2]))
        
