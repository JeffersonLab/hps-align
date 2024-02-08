
from ._utils import *
from ._uchannel import UChannel
from ._sensors import *
from ._mattsensor import *
from ._ballframe import *
from ._pinframe import *
from ._cli import app


class Survey:
    """SVT survey class

    This class combines the UChannel and sensor measurements.
    Depending on the configuration of the SVT, this class contains a different set of sensors.

    Attributes
    ----------
    uchannel : UChannel
        UChannel object
    sensors : dict
        Dictionary of sensors {volume: {layer: {sensor (ax/st): Sensor()}}}
    """
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
    """SVT survey class for 2019 configuration

    Here, only the first two layers in top and bottom are used.
    """
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

        self.fixture = Fixture(survey_files['fixture'])
        self.transition_fixture = Fixture(survey_files['transition_fixture'])

        L0_axial_top = MattSensor(self.transition_fixture, survey_files['L0_axial_top'])
        L0_stereo_top = MattSensor(self.transition_fixture, survey_files['L0_stereo_top'])
        L1_axial_top = MattSensor(self.transition_fixture, survey_files['L1_axial_top'])
        L1_stereo_top = MattSensor(self.transition_fixture, survey_files['L1_stereo_top'])

        L0_axial_bottom = MattSensor(self.transition_fixture, survey_files['L0_axial_bottom'])
        L0_stereo_bottom = MattSensor(self.transition_fixture, survey_files['L0_stereo_bottom'])
        L1_axial_bottom = MattSensor(self.transition_fixture, survey_files['L1_axial_bottom'])
        L1_stereo_bottom = MattSensor(self.transition_fixture, survey_files['L1_stereo_bottom'])

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
        """Get pin frame basis vectors and origin in uchannel ball frame
        
        To attach the L2 slim sensors a transition plate is used. This transition plate has a
        different pin frame (small pin frame) than the original L2 uchannel pins (wide pin frame).
        To account for this, additional coordinate transformations are needed.
        For L1, the uchannel pin frame is already the small pin frame, hence no transformation is needed.

        Parameters
        ----------
        volume : str
            Volume ('top' or 'bottom')
        layer : int
            Layer number
        
        Returns
        -------
        basis : np.array
            Basis vectors in uchannel ball frame
        origin : np.array
            Origin in uchannel ball frame
        """
        if layer == 1:
            # pin frame in ogp coordinates
            pin_basis, pin_origin = self.uchannel.get_pin_basis(layer, volume)
            # ball frame in ogp coordinates
            ball_basis, ball_origin = self.uchannel.get_ball_basis(volume)

            # wide fixture pin frame in ogp coordinates
            wide_fixture_basis = self.fixture.get_pin_basis()[0]
            # small fixture pin frame in ogp coordinates
            small_fixture_basis = self.transition_fixture.get_pin_basis()[0]

            # rotation of basis vectors from small fixture pin frame to wide fixture pin frame
            small_to_wide = np.matmul(small_fixture_basis, np.linalg.inv(wide_fixture_basis))
            # small fixture pin frame in uchannel pin frame (= wide fixture pin frame) coordinates
            pin_small_basis = np.matmul(small_to_wide, pin_basis)

            # rotation of basis vectors from pin frame to uchannel ball frame
            basis = np.matmul(pin_small_basis, np.linalg.inv(ball_basis))

            if volume == 'top' and self.uchannel.ballframe_top.__class__.__name__ == 'MattBallFrame':
                origin = pin_origin
            elif volume == 'bottom' and self.uchannel.ballframe_bot.__class__.__name__ == 'MattBallFrame':
                origin = pin_origin
            else:
                # translation of origin in ball frame
                origin = pin_origin - ball_origin

            wide_pin_fixball_basis, wide_pin_fixball_origin = self.fixture.get_pin_in_ball()
            small_pin_fixball_origin = self.transition_fixture.get_pin_in_ball()[1]

            # translation vector between pin frames in fixture ball frame
            wide_to_small_fixball = small_pin_fixball_origin - wide_pin_fixball_origin
            # translation vector between pin frames in uchannel pin frame
            wide_to_small_pin = np.matmul(wide_to_small_fixball, np.linalg.inv(wide_pin_fixball_basis))
            # translation vector between pin frames in uchannel ball frame
            wide_to_small_ball = np.matmul(wide_to_small_pin, np.matmul(pin_basis, np.linalg.inv(ball_basis)))

            # origin in uchannel ball frame
            origin = np.matmul(origin, np.linalg.inv(ball_basis)) + wide_to_small_ball

            return basis, origin

        else:
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
        """Print results to file

        Writes pin frame basis vectors and origins in uchannel ball frame
        and sensor basis vectors and origins in pin frame to file.

        Parameters
        ----------
        out_name : str
            Output file name
        """
        with open(out_name, 'w') as f:
            for volume in ['top', 'bottom']:
                if volume == 'top':
                    short_name = 't'
                else:
                    short_name = 'b'
                for layer in [1, 2]:
                    f.write('<SurveyVolume name="module_L' + str(layer) + short_name + '" desc="'
                            + volume + ' L' + str(layer) + ' pin basis in U-channel fiducial frame:">\n')
                    basis, origin = self.get_pin_in_uchannel_ballframe(volume, layer-1)
                    f.write('<origin x="' + str(origin[0]) + '" y="' + str(origin[1]) + '" z="' + str(origin[2]) + '" />\n')
                    f.write('<unitvec name="X" x="' + str(basis[0][0]) + '" y="' + str(basis[0][1])
                            + '" z="' + str(basis[0][2]) + '" />\n')
                    f.write('<unitvec name="Y" x="' + str(basis[1][0]) + '" y="' + str(basis[1][1])
                            + '" z="' + str(basis[1][2]) + '" />\n')
                    f.write('<unitvec name="Z" x="' + str(basis[2][0]) + '" y="' + str(basis[2][1])
                            + '" z="' + str(basis[2][2]) + '" />\n')
                    f.write('</SurveyVolume>\n')

                    for sensor in ['axial', 'stereo']:
                        # print('volume ', volume, ' layer ', layer, ' sensor ', sensor)
                        f.write('<SurveyVolume name="module_L' + str(layer) + short_name + '_halfmodule_' + sensor
                                + '" desc="' + volume + ' L' + str(layer) + ' ' + sensor + ' sensor basis in pin frame:">\n')
                        sensor_basis_pin, sensor_origin_pin = self.sensors[volume][str(layer-1)][sensor].get_sensor_basis_pinframe()
                        f.write('<origin x="' + str(sensor_origin_pin[0]) + '" y="' + str(sensor_origin_pin[1])
                                + '" z="' + str(sensor_origin_pin[2]) + '" />\n')
                        f.write('<unitvec name="X" x="' + str(sensor_basis_pin[0][0]) + '" y="' + str(sensor_basis_pin[0][1])
                                + '" z="' + str(sensor_basis_pin[0][2]) + '" />\n')
                        f.write('<unitvec name="Y" x="' + str(sensor_basis_pin[1][0]) + '" y="' + str(sensor_basis_pin[1][1])
                                + '" z="' + str(sensor_basis_pin[1][2]) + '" />\n')
                        f.write('<unitvec name="Z" x="' + str(sensor_basis_pin[2][0]) + '" y="' + str(sensor_basis_pin[2][1])
                                + '" z="' + str(sensor_basis_pin[2][2]) + '" />\n')
                        f.write('</SurveyVolume>\n')
