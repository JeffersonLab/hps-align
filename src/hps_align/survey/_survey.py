
from ._utils import *
from ._uchannel import UChannel
from ._sensors import *
from ._ballframe import *
from ._pinframe import *
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
            for volume in ['top', 'bottom']:
                if volume == 'top':
                    short_name = 't'
                else:
                    short_name = 'b'
                for layer in [1,2]:
                    f.write('<SurveyVolume name="module_L' + str(layer) + short_name + '" desc="' + volume + ' L' + str(layer) + ' pin basis in U-channel fiducial frame:">\n')
                    basis, origin = self.get_pin_in_uchannel_ballframe(volume, layer-1)
                    f.write('<origin x="' + str(origin[0]) + '" y="' + str(origin[1]) + '" z="' + str(origin[2]) + '" />\n')
                    f.write('<unitvec name="X" x="' + str(basis[0][0]) + '" y="' + str(basis[0][1]) + '" z="' + str(basis[0][2]) + '" />\n')
                    f.write('<unitvec name="Y" x="' + str(basis[1][0]) + '" y="' + str(basis[1][1]) + '" z="' + str(basis[1][2]) + '" />\n')
                    f.write('<unitvec name="Z" x="' + str(basis[2][0]) + '" y="' + str(basis[2][1]) + '" z="' + str(basis[2][2]) + '" />\n')
                    f.write('</SurveyVolume>\n')

                    for sensor in ['axial', 'stereo']:
                        f.write('<SurveyVolume name="module_L' + str(layer) + short_name + '_halfmodule_' + sensor +'" desc="' + volume + ' L' + str(layer) + ' ' + sensor +' sensor basis in pin frame:">\n')
                        sensor_basis_pin, sensor_origin_pin = self.sensors[volume][str(layer-1)][sensor].get_sensor_basis_pinframe(volume, sensor)
                        f.write('<origin x="' + str(sensor_origin_pin[0]) + '" y=" ' + str(sensor_origin_pin[1]) + '" z="' + str(sensor_origin_pin[2]) + '" />\n')
                        f.write('<unitvec name="X" x="' + str(sensor_basis_pin[0][0]) + '" y="' + str(sensor_basis_pin[0][1]) + '" z="' + str(sensor_basis_pin[0][2]) + '" />\n')
                        f.write('<unitvec name="Y" x="' + str(sensor_basis_pin[1][0]) + '" y="' + str(sensor_basis_pin[1][1]) + '" z="' + str(sensor_basis_pin[1][2]) + '" />\n')
                        f.write('<unitvec name="Z" x="' + str(sensor_basis_pin[2][0]) + '" y="' + str(sensor_basis_pin[2][1]) + '" z="' + str(sensor_basis_pin[2][2]) + '" />\n')
                        f.write('</SurveyVolume>\n')