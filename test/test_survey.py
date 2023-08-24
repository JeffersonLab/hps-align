
import unittest

from hps_align.survey._sensors import *
from hps_align.survey._uchannel import *
from hps_align.survey._ballframe import *
from hps_align.survey._pinframe import *
from hps_align.survey._baseplanes import *
from hps_align.survey._survey import *


class TestPinInUchannelBallframe(unittest.TestCase):

    def test_top(self):
        pin = Pin()
        pin.set_pin({'x': 1, 'y': 2, 'z': 0}, 1, 'hole')
        pin.set_pin({'x': 5, 'y': 2, 'z': 0}, 1, 'slot')

        baseplane = BasePlane()
        baseplane.set_base_plane_dict({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2}, 1)

        pinframe = PinFrame()
        pinframe.pins = pin
        pinframe.base_planes = baseplane
        # gives pin_basis [[-1, 0, 0], [0, 0, 1], [0, 1, 0]]

        ballframe = BallFrame()
        ballframe.set_ball({'x': 0, 'y': 1, 'z': 1}, 1, 'hole')
        ballframe.set_ball({'x': 6, 'y': 1, 'z': 1}, 1, 'slot')
        ballframe.set_ball({'x': 0, 'y': 5, 'z': 1}, 3, 'hole')
        ballframe.set_ball({'x': 6, 'y': 5, 'z': 1}, 3, 'slot')
        # gives ball_basis [[1, 0, 0], [0, 0, -1], [0, 1, 0]]

        uchannel = UChannel(pinframe_top=pinframe, ballframe_top=ballframe)

        survey = Survey()
        survey.set_uchannel(uchannel)

        basis, origin = survey.get_pin_in_uchannel_ballframe('top', 1)

        self.assertAlmostEqual(-2, origin[0])
        self.assertAlmostEqual(1, origin[1])
        self.assertAlmostEqual(1, origin[2])
        self.assertAlmostEqual(-1, basis[0][0])
        self.assertAlmostEqual(0, basis[0][1])
        self.assertAlmostEqual(0, basis[0][2])
        self.assertAlmostEqual(0, basis[1][0])
        self.assertAlmostEqual(-1, basis[1][1])
        self.assertAlmostEqual(0, basis[1][2])
        self.assertAlmostEqual(0, basis[2][0])
        self.assertAlmostEqual(0, basis[2][1])
        self.assertAlmostEqual(1, basis[2][2])


class TestTransformSensorToUchannelBallframe(unittest.TestCase):

    def test_top(self):
        pin = Pin()
        pin.set_pin({'x': 1, 'y': 2, 'z': 0}, 1, 'hole')
        pin.set_pin({'x': 5, 'y': 2, 'z': 0}, 1, 'slot')

        baseplane = BasePlane()
        baseplane.set_base_plane_dict({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2}, 1)

        pinframe = PinFrame()
        pinframe.pins = pin
        pinframe.base_planes = baseplane
        # gives pin_basis [[-1, 0, 0], [0, 0, 1], [0, 1, 0]]

        ballframe = BallFrame()
        ballframe.set_ball({'x': 0, 'y': 1, 'z': 1}, 1, 'hole')
        ballframe.set_ball({'x': 6, 'y': 1, 'z': 1}, 1, 'slot')
        ballframe.set_ball({'x': 0, 'y': 5, 'z': 1}, 3, 'hole')
        ballframe.set_ball({'x': 6, 'y': 5, 'z': 1}, 3, 'slot')
        # gives ball_basis [[1, 0, 0], [0, 0, -1], [0, 1, 0]]

        uchannel = UChannel(pinframe_top=pinframe, ballframe_top=ballframe)

        fixture = Fixture()
        fixture.set_ball({'x': 1, 'y': 1, 'z': 5}, 'oriball')
        fixture.set_ball({'x': 8, 'y': 1, 'z': 5}, 'axiball')
        fixture.set_ball({'x': 1, 'y': 1, 'z': 6}, 'diagball')
        fixture.set_pin({'x': 2, 'y': 1, 'z': 1}, 'oripin')
        fixture.set_pin({'x': 7, 'y': 1, 'z': 1}, 'axipin')
        fixture.set_base_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2})

        stereo_sensor = Sensor(fixture)
        stereo_sensor.set_ball({'x': 1, 'y': 1, 'z': 0}, 'oriball')
        stereo_sensor.set_ball({'x': 8, 'y': 1, 'z': 0}, 'axiball')
        stereo_sensor.set_ball({'x': 1, 'y': 2, 'z': 0}, 'diagball')
        stereo_sensor.set_sensor_plane({'x': 4, 'y': 1, 'z': 1, 'xy_angle': 0, 'elevation': np.pi/2})
        stereo_sensor.set_sensor_origin({'x': 4, 'y': 1, 'z': 1})

        axial_sensor = Sensor(fixture)
        axial_sensor.set_ball({'x': 8, 'y': 1, 'z': 0}, 'oriball')
        axial_sensor.set_ball({'x': 1, 'y': 1, 'z': 0}, 'axiball')
        axial_sensor.set_ball({'x': 8, 'y': 2, 'z': 0}, 'diagball')
        axial_sensor.set_sensor_plane({'x': 4, 'y': 1, 'z': 1, 'xy_angle': 0, 'elevation': np.pi/2})
        axial_sensor.set_sensor_origin({'x': 4, 'y': 1, 'z': 1})

        stereo_origin_ball = stereo_sensor.get_sensor_origin_ballframe()
        self.assertAlmostEqual(3, stereo_origin_ball[0])
        self.assertAlmostEqual(0, stereo_origin_ball[1])
        self.assertAlmostEqual(1, stereo_origin_ball[2])

        stereo_origin_pin = stereo_sensor.get_sensor_origin_pinframe()
        self.assertAlmostEqual(-3, stereo_origin_pin[0])
        self.assertAlmostEqual(5, stereo_origin_pin[1])
        self.assertAlmostEqual(1, stereo_origin_pin[2])

        axial_origin_ball = axial_sensor.get_sensor_origin_ballframe()
        self.assertAlmostEqual(4, axial_origin_ball[0])
        self.assertAlmostEqual(0, axial_origin_ball[1])
        self.assertAlmostEqual(-1, axial_origin_ball[2])

        axial_origin_pin = axial_sensor.get_sensor_origin_pinframe()
        self.assertAlmostEqual(-2, axial_origin_pin[0])
        self.assertAlmostEqual(5, axial_origin_pin[1])
        self.assertAlmostEqual(-1, axial_origin_pin[2])

        stereo_normal_ball = stereo_sensor.get_sensor_normal_ballframe()
        self.assertAlmostEqual(0, stereo_normal_ball[0])
        self.assertAlmostEqual(0, stereo_normal_ball[1])
        self.assertAlmostEqual(1, stereo_normal_ball[2])

        stereo_normal_pin = stereo_sensor.get_sensor_normal_pinframe()
        self.assertAlmostEqual(0, stereo_normal_pin[0])
        self.assertAlmostEqual(0, stereo_normal_pin[1])
        self.assertAlmostEqual(1, stereo_normal_pin[2])

        axial_normal_ball = axial_sensor.get_sensor_normal_ballframe()
        self.assertAlmostEqual(0, axial_normal_ball[0])
        self.assertAlmostEqual(0, axial_normal_ball[1])
        self.assertAlmostEqual(-1, axial_normal_ball[2])

        axial_normal_pin = axial_sensor.get_sensor_normal_pinframe()
        self.assertAlmostEqual(0, axial_normal_pin[0])
        self.assertAlmostEqual(0, axial_normal_pin[1])
        self.assertAlmostEqual(-1, axial_normal_pin[2])

        survey = Survey()
        survey.set_uchannel(uchannel)
        survey.set_sensors({'top': {'1': {'stereo': stereo_sensor, 'axial': axial_sensor}}, 'bottom': {}})

        sensor_origin_ball, sensor_normal_ball = survey.transform_sensor_to_uchannel_ballframe('top', '1', 'stereo')

        self.assertAlmostEqual(1, sensor_origin_ball[0])
        self.assertAlmostEqual(-4, sensor_origin_ball[1])
        self.assertAlmostEqual(2, sensor_origin_ball[2])
        self.assertAlmostEqual(0, sensor_normal_ball[0])
        self.assertAlmostEqual(0, sensor_normal_ball[1])
        self.assertAlmostEqual(1, sensor_normal_ball[2])

        sensor_origin_ball, sensor_normal_ball = survey.transform_sensor_to_uchannel_ballframe('top', '1', 'axial')

        self.assertAlmostEqual(0, sensor_origin_ball[0])
        self.assertAlmostEqual(-4, sensor_origin_ball[1])
        self.assertAlmostEqual(0, sensor_origin_ball[2])
        self.assertAlmostEqual(0, sensor_normal_ball[0])
        self.assertAlmostEqual(0, sensor_normal_ball[1])
        self.assertAlmostEqual(-1, sensor_normal_ball[2])

    def test_bottom(self):
        pin = Pin()
        pin.set_pin({'x': 1, 'y': 2, 'z': 0}, 1, 'slot')
        pin.set_pin({'x': 5, 'y': 2, 'z': 0}, 1, 'hole')

        baseplane = BasePlane()
        baseplane.set_base_plane_dict({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2}, 1)

        pinframe = PinFrame()
        pinframe.pins = pin
        pinframe.base_planes = baseplane
        # gives pin_basis [[1, 0, 0], [0, 0, 1], [0, -1, 0]]

        ballframe = BallFrame()
        ballframe.set_ball({'x': 0, 'y': 1, 'z': 1}, 1, 'slot')
        ballframe.set_ball({'x': 6, 'y': 1, 'z': 1}, 1, 'hole')
        ballframe.set_ball({'x': 0, 'y': 5, 'z': 1}, 3, 'slot')
        ballframe.set_ball({'x': 6, 'y': 5, 'z': 1}, 3, 'hole')
        # gives ball_basis [[-1, 0, 0], [0, 0, 1], [0, 1, 0]]

        uchannel = UChannel(pinframe_bot=pinframe, ballframe_bot=ballframe)

        fixture = Fixture()
        fixture.set_ball({'x': 1, 'y': 1, 'z': 5}, 'oriball')
        fixture.set_ball({'x': 8, 'y': 1, 'z': 5}, 'axiball')
        fixture.set_ball({'x': 1, 'y': 1, 'z': 6}, 'diagball')
        fixture.set_pin({'x': 2, 'y': 1, 'z': 1}, 'oripin')
        fixture.set_pin({'x': 7, 'y': 1, 'z': 1}, 'axipin')
        fixture.set_base_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2})

        axial_sensor = Sensor(fixture)
        axial_sensor.set_ball({'x': 1, 'y': 1, 'z': 0}, 'oriball')
        axial_sensor.set_ball({'x': 8, 'y': 1, 'z': 0}, 'axiball')
        axial_sensor.set_ball({'x': 1, 'y': 2, 'z': 0}, 'diagball')
        axial_sensor.set_sensor_plane({'x': 4, 'y': 1, 'z': 1, 'xy_angle': 0, 'elevation': np.pi/2})
        axial_sensor.set_sensor_origin({'x': 4, 'y': 1, 'z': 1})

        stereo_sensor = Sensor(fixture)
        stereo_sensor.set_ball({'x': 8, 'y': 1, 'z': 0}, 'oriball')
        stereo_sensor.set_ball({'x': 1, 'y': 1, 'z': 0}, 'axiball')
        stereo_sensor.set_ball({'x': 8, 'y': 2, 'z': 0}, 'diagball')
        stereo_sensor.set_sensor_plane({'x': 4, 'y': 1, 'z': 1, 'xy_angle': 0, 'elevation': np.pi/2})
        stereo_sensor.set_sensor_origin({'x': 4, 'y': 1, 'z': 1})

        stereo_origin_ball = stereo_sensor.get_sensor_origin_ballframe()
        self.assertAlmostEqual(4, stereo_origin_ball[0])
        self.assertAlmostEqual(0, stereo_origin_ball[1])
        self.assertAlmostEqual(-1, stereo_origin_ball[2])

        stereo_origin_pin = stereo_sensor.get_sensor_origin_pinframe()
        self.assertAlmostEqual(-2, stereo_origin_pin[0])
        self.assertAlmostEqual(5, stereo_origin_pin[1])
        self.assertAlmostEqual(-1, stereo_origin_pin[2])

        axial_origin_ball = axial_sensor.get_sensor_origin_ballframe()
        self.assertAlmostEqual(3, axial_origin_ball[0])
        self.assertAlmostEqual(0, axial_origin_ball[1])
        self.assertAlmostEqual(1, axial_origin_ball[2])

        axial_origin_pin = axial_sensor.get_sensor_origin_pinframe()
        self.assertAlmostEqual(-3, axial_origin_pin[0])
        self.assertAlmostEqual(5, axial_origin_pin[1])
        self.assertAlmostEqual(1, axial_origin_pin[2])

        stereo_normal_ball = stereo_sensor.get_sensor_normal_ballframe()
        self.assertAlmostEqual(0, stereo_normal_ball[0])
        self.assertAlmostEqual(0, stereo_normal_ball[1])
        self.assertAlmostEqual(-1, stereo_normal_ball[2])

        stereo_normal_pin = stereo_sensor.get_sensor_normal_pinframe()
        self.assertAlmostEqual(0, stereo_normal_pin[0])
        self.assertAlmostEqual(0, stereo_normal_pin[1])
        self.assertAlmostEqual(-1, stereo_normal_pin[2])

        axial_normal_ball = axial_sensor.get_sensor_normal_ballframe()
        self.assertAlmostEqual(0, axial_normal_ball[0])
        self.assertAlmostEqual(0, axial_normal_ball[1])
        self.assertAlmostEqual(1, axial_normal_ball[2])

        axial_normal_pin = axial_sensor.get_sensor_normal_pinframe()
        self.assertAlmostEqual(0, axial_normal_pin[0])
        self.assertAlmostEqual(0, axial_normal_pin[1])
        self.assertAlmostEqual(1, axial_normal_pin[2])

        survey = Survey()
        survey.set_uchannel(uchannel)
        survey.set_sensors({'bottom': {'1': {'axial': axial_sensor, 'stereo': stereo_sensor}}, 'top': {}})

        sensor_origin_ball, sensor_normal_ball = survey.transform_sensor_to_uchannel_ballframe('bottom', '1', 'stereo')

        self.assertAlmostEqual(0, sensor_origin_ball[0])
        self.assertAlmostEqual(4, sensor_origin_ball[1])
        self.assertAlmostEqual(2, sensor_origin_ball[2])
        self.assertAlmostEqual(0, sensor_normal_ball[0])
        self.assertAlmostEqual(0, sensor_normal_ball[1])
        self.assertAlmostEqual(1, sensor_normal_ball[2])

        sensor_origin_ball, sensor_normal_ball = survey.transform_sensor_to_uchannel_ballframe('bottom', '1', 'axial')

        self.assertAlmostEqual(1, sensor_origin_ball[0])
        self.assertAlmostEqual(4, sensor_origin_ball[1])
        self.assertAlmostEqual(0, sensor_origin_ball[2])
        self.assertAlmostEqual(0, sensor_normal_ball[0])
        self.assertAlmostEqual(0, sensor_normal_ball[1])
        self.assertAlmostEqual(-1, sensor_normal_ball[2])


# class TestSurvey2019(unittest.TestCase):

#     def test_txt_input(self):
#         survey_files = {'ballframe_top': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_empty_top_1.txt',
#                         'pinframe_top': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_empty_top_1.txt',
#                         'ballframe_bottom': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_empty_bottom_1.txt',
#                         'pinframe_bottom': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_empty_bottom_1.txt',
#                         'matt_fixture': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L0_fixture_empty_1.txt',
#                         'sho_fixture': '/Users/schababi/workspace/hps/hps-align/survey_data/L123_fixture_sho.txt',
#                         'L0_axial_top': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L0_axial_top_module1_1.txt',
#                         'L0_stereo_top': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L0_stereo_top_module1_1.txt',
#                         'L0_axial_bottom': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L0_axial_bottom_module2_1.txt',
#                         'L0_stereo_bottom': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L0_stereo_bottom_module2_1.txt',
#                         'L1_axial_top': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L1_axial_top_module3_1.txt',
#                         'L1_stereo_top': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L1_stereo_top_module3_1.txt',
#                         'L1_axial_bottom': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L1_axial_bottom_module5_1.txt',
#                         'L1_stereo_bottom': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L1_stereo_bottom_module5_1.txt'}

#         survey = Survey2019(survey_files)

#         print('\npin in uchannel, L1 top: ', survey.get_pin_in_uchannel_ballframe('top', '1')[1])
#         # print('pin in uchannel, L2 top: ', survey.get_pin_in_uchannel_ballframe('top', '2')[1])
#         # print('pin in uchannel, L3 top: ', survey.get_pin_in_uchannel_ballframe('top', '3')[1])
#         # print('pin in uchannel, L1 bottom: ', survey.get_pin_in_uchannel_ballframe('bottom', '1')[1])
#         # print('pin in uchannel, L2 bottom: ', survey.get_pin_in_uchannel_ballframe('bottom', '2')[1])
#         # print('pin in uchannel, L3 bottom: ', survey.get_pin_in_uchannel_ballframe('bottom', '3')[1])
#         print('pin in uchannel, L0 top: ', survey.get_pin_in_uchannel_ballframe('top', '1')[1])
#         sensor_origin_ball = survey.transform_sensor_to_uchannel_ballframe('top', '1', 'stereo')
#         print('sensor in uchannel: ', sensor_origin_ball)
#         survey.print_results('survey_results_2019.csv')
