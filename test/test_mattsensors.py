
import unittest
import numpy as np

from hps_align.survey._sensors import MattSensor
from hps_align.survey._fixture import Fixture


class TestInit(unittest.TestCase):

    def test_no_input(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        with self.assertWarns(UserWarning):
            sensor = MattSensor(fixture)

        empty_dict = {'x': 0, 'y': 0, 'z': 0}
        empty_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0}
        self.assertEqual(empty_dict, sensor.oriball_dict)
        self.assertEqual(empty_dict, sensor.diagball_dict)
        self.assertEqual(empty_dict, sensor.axiball_dict)
        self.assertEqual(empty_plane_dict, sensor.ball_plane_dict)
        self.assertEqual(empty_dict, sensor.sensor_origin_dict)
        self.assertEqual(empty_plane_dict, sensor.sensor_plane_dict)
        self.assertEqual(empty_dict, sensor.fixture.oriball_dict)
        self.assertEqual(empty_dict, sensor.fixture.diagball_dict)
        self.assertEqual(empty_dict, sensor.fixture.axiball_dict)
        self.assertEqual(empty_dict, sensor.fixture.oripin_dict)
        self.assertEqual(empty_dict, sensor.fixture.axipin_dict)
        self.assertEqual(empty_plane_dict, sensor.fixture.base_plane_dict)


class TestMattToBall(unittest.TestCase):

    def test_get_matt_basis(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        with self.assertWarns(UserWarning):
            sensor = MattSensor(fixture)
        
        sensor.set_ball({'x': 0, 'y': 0, 'z': 0}, 'oriball')
        sensor.set_ball({'x': 5, 'y': 0, 'z': 0}, 'axiball')
        sensor.set_ball({'x': 0, 'y': 1, 'z': 1}, 'diagball')
        sensor.ball_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2}

        basis, origin = sensor.get_matt_basis()
        self.assertEqual([1, 0, 0], basis[0].tolist())
        self.assertEqual([0, 1, 0], basis[1].tolist())
        self.assertEqual([0, 0, 1], basis[2].tolist())
        self.assertEqual([0, 0, 0], origin.tolist())

    def test_same_system(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        with self.assertWarns(UserWarning):
            sensor = MattSensor(fixture)

        sensor.set_ball({'x': 1, 'y': 0, 'z': 0}, 'oriball')
        sensor.set_ball({'x': 1, 'y': 1, 'z': 0}, 'axiball')
        sensor.set_ball({'x': 1, 'y': 0, 'z': 1}, 'diagball')

        basis = sensor.matt_to_ball()
        self.assertEqual([1, 0, 0], basis[0].tolist())
        self.assertEqual([0, 1, 0], basis[1].tolist())
        self.assertEqual([0, 0, 1], basis[2].tolist())

    def test_different_systems(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        with self.assertWarns(UserWarning):
            sensor = MattSensor(fixture)
        
        sensor.set_ball({'x': 0, 'y': 0, 'z': 0}, 'oriball')
        sensor.set_ball({'x': 5, 'y': 0, 'z': 0}, 'axiball')
        sensor.set_ball({'x': 0, 'y': -1, 'z': 0}, 'diagball')
        sensor.ball_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2}

        basis = sensor.matt_to_ball()
        self.assertEqual([1, 0, 0], basis[0].tolist())
        self.assertEqual([0, -1, 0], basis[1].tolist())
        self.assertEqual([0, 0, -1], basis[2].tolist())


class TestSensorOrigin(unittest.TestCase):

    def test_get_sensor_origin_ballframe(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        with self.assertWarns(UserWarning):
            sensor = MattSensor(fixture)

        sensor.set_ball({'x': 1, 'y': 0, 'z': 0}, 'oriball')
        sensor.set_ball({'x': 1, 'y': 1, 'z': 0}, 'axiball')
        sensor.set_ball({'x': 1, 'y': 0, 'z': 1}, 'diagball')
        sensor.set_sensor_origin({'x': 1, 'y': 2, 'z': 3})

        self.assertEqual([1, 2, 3], sensor.get_sensor_origin_ballframe().tolist())

    def test_get_sensor_origin_pinframe(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()
            fixture.set_ball({'x': 1, 'y': 0, 'z': 0}, 'oriball')
            fixture.set_ball({'x': 1, 'y': 1, 'z': 0}, 'axiball')
            fixture.set_ball({'x': 1, 'y': 0, 'z': 1}, 'diagball')
            fixture.set_pin({'x': 1, 'y': 0, 'z': 1}, 'oripin')
            fixture.set_pin({'x': 1, 'y': 1, 'z': 1}, 'axipin')
            fixture.set_base_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2})

        with self.assertWarns(UserWarning):
            sensor = MattSensor(fixture)

        sensor.set_ball({'x': 1, 'y': 0, 'z': 0}, 'oriball')
        sensor.set_ball({'x': 1, 'y': 1, 'z': 0}, 'axiball')
        sensor.set_ball({'x': 1, 'y': 0, 'z': 1}, 'diagball')
        sensor.set_sensor_origin({'x': 1, 'y': 2, 'z': 3})

        origin_pin = sensor.get_sensor_origin_pinframe()
        self.assertAlmostEqual(0, origin_pin[0])
        self.assertAlmostEqual(2, origin_pin[1])
        self.assertAlmostEqual(-3, origin_pin[2])


class TestSensorNormal(unittest.TestCase):

    def test_get_sensor_normal_ballframe(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        with self.assertWarns(UserWarning):
            sensor = MattSensor(fixture)

        sensor.set_ball({'x': 1, 'y': 0, 'z': 0}, 'oriball')
        sensor.set_ball({'x': 1, 'y': 1, 'z': 0}, 'axiball')
        sensor.set_ball({'x': 1, 'y': 0, 'z': 1}, 'diagball')
        sensor.set_sensor_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0})

        normal_ball = sensor.get_sensor_normal_ballframe()
        self.assertAlmostEqual(1, normal_ball[0])
        self.assertAlmostEqual(0, normal_ball[1])
        self.assertAlmostEqual(0, normal_ball[2])

    def test_get_sensor_normal_pinframe(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()
            fixture.set_ball({'x': 1, 'y': 1, 'z': 5}, 'oriball')
            fixture.set_ball({'x': 7, 'y': 1, 'z': 5}, 'axiball')
            fixture.set_ball({'x': 1, 'y': 1, 'z': 6}, 'diagball')
            fixture.set_pin({'x': 2, 'y': 1, 'z': 1}, 'oripin')
            fixture.set_pin({'x': 5, 'y': 1, 'z': 1}, 'axipin')
            fixture.set_base_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2})

        with self.assertWarns(UserWarning):
            sensor = MattSensor(fixture)

        sensor.set_ball({'x': 1, 'y': 1, 'z': 0}, 'oriball')
        sensor.set_ball({'x': 7, 'y': 1, 'z': 0}, 'axiball')
        sensor.set_ball({'x': 1, 'y': 2, 'z': 0}, 'diagball')
        sensor.set_sensor_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0})

        normal = sensor.get_sensor_normal_pinframe()
        self.assertAlmostEqual(-1, normal[0])
        self.assertAlmostEqual(0, normal[1])
        self.assertAlmostEqual(0, normal[2])

    # def test_input_file(self):
    #     sensor = Sensor('/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L0_axial1_1.txt',
    #                     '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L0_fixture_empty_1.txt')

    #     origin_bot = sensor.get_sensor_origin_pinframe('bottom', True)
    #     origin_top = sensor.get_sensor_origin_pinframe('top', True)

    #     print('bottom origin: ', origin_bot)
    #     print('top origin: ', origin_top)


if __name__ == '__main__':
    unittest.main()
