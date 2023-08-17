
import unittest
import numpy as np

from hps_align.survey._sensors import MattSensor
from hps_align.survey._fixture import *


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

        sensor.set_ball({'x': 0, 'y': 0, 'z': 0}, 'oriball')
        sensor.set_ball({'x': 5, 'y': 0, 'z': 0}, 'axiball')
        sensor.set_ball({'x': 0, 'y': 1, 'z': 1}, 'diagball')
        sensor.ball_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2}

        basis = sensor.matt_to_ball()
        self.assertEqual([1, 0, 0], basis[0].tolist())
        self.assertAlmostEqual(0, basis[1][0])
        self.assertAlmostEqual(1/np.sqrt(2), basis[1][1])
        self.assertAlmostEqual(-1/np.sqrt(2), basis[1][2])
        self.assertAlmostEqual(0, basis[2][0])
        self.assertAlmostEqual(1/np.sqrt(2), basis[2][1])
        self.assertAlmostEqual(1/np.sqrt(2), basis[2][2])


class TestSensorOrigin(unittest.TestCase):

    def test_get_sensor_origin_ballframe(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        with self.assertWarns(UserWarning):
            sensor = MattSensor(fixture)

        sensor.set_ball({'x': 1, 'y': 0, 'z': 0}, 'oriball')
        sensor.set_ball({'x': 1, 'y': 1, 'z': 0}, 'axiball')
        sensor.set_ball({'x': 1, 'y': 0, 'z': 1}, 'diagball')
        sensor.ball_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2}  # ball plane normal in global z
        sensor.set_sensor_origin({'x': 1, 'y': 2, 'z': 3})  # in Matt frame

        origin = sensor.get_sensor_origin_ballframe()
        self.assertAlmostEqual(1, origin[0])
        self.assertAlmostEqual(3, origin[1])
        self.assertAlmostEqual(-2, origin[2])

    def test_get_sensor_origin_pinframe(self):
        with self.assertWarns(UserWarning):
            fixture = MattFixture()
            fixture.set_ball({'x': 1, 'y': 0, 'z': 0}, 'oriball')
            fixture.set_ball({'x': 1, 'y': 3, 'z': 0}, 'axiball')
            fixture.set_ball({'x': 1, 'y': 0, 'z': 2}, 'diagball')
            fixture.ball_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2}  # ball plane normal in global z
            # in Matt frame:
            fixture.set_pin({'x': 1, 'y': 0, 'z': 1}, 'oripin')
            fixture.set_pin({'x': 2, 'y': 0, 'z': 1}, 'axipin')
            fixture.set_base_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 3*np.pi/2, 'elevation': 0})

        with self.assertWarns(UserWarning):
            sensor = MattSensor(fixture)

        sensor.set_ball({'x': 1, 'y': 0, 'z': 0}, 'oriball')
        sensor.set_ball({'x': 1, 'y': 1, 'z': 0}, 'axiball')
        sensor.set_ball({'x': 1, 'y': 0, 'z': 1}, 'diagball')
        sensor.ball_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2}  # ball plane normal in global z
        sensor.set_sensor_origin({'x': 1, 'y': -1, 'z': 0})

        origin_pin = sensor.get_sensor_origin_pinframe()
        self.assertAlmostEqual(-1, origin_pin[0])
        self.assertAlmostEqual(1, origin_pin[1])
        self.assertAlmostEqual(1, origin_pin[2])


class TestSensorNormal(unittest.TestCase):

    def test_get_sensor_normal_ballframe(self):
        with self.assertWarns(UserWarning):
            fixture = MattFixture()

        with self.assertWarns(UserWarning):
            sensor = MattSensor(fixture)

        sensor.set_ball({'x': 1, 'y': 0, 'z': 0}, 'oriball')
        sensor.set_ball({'x': 1, 'y': 1, 'z': 0}, 'axiball')
        sensor.set_ball({'x': 1, 'y': 0, 'z': 1}, 'diagball')
        sensor.ball_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2}  # ball plane normal in global z
        # in Matt frame:
        sensor.set_sensor_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0})

        normal_ball = sensor.get_sensor_normal_ballframe()
        self.assertAlmostEqual(1, normal_ball[0])
        self.assertAlmostEqual(0, normal_ball[1])
        self.assertAlmostEqual(0, normal_ball[2])

    def test_get_sensor_normal_pinframe(self):
        with self.assertWarns(UserWarning):
            fixture = MattFixture()
            fixture.set_ball({'x': 1, 'y': 1, 'z': 5}, 'oriball')
            fixture.set_ball({'x': 7, 'y': 1, 'z': 5}, 'axiball')
            fixture.set_ball({'x': 1, 'y': 1, 'z': 6}, 'diagball')
            fixture.ball_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2}  # ball plane normal in global z
            # in Matt frame:
            fixture.set_pin({'x': 2, 'y': 2, 'z': 1}, 'oripin')
            fixture.set_pin({'x': 5, 'y': 2, 'z': 1}, 'axipin')
            fixture.set_base_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2})

        with self.assertWarns(UserWarning):
            sensor = MattSensor(fixture)

        sensor.set_ball({'x': 1, 'y': 1, 'z': 0}, 'oriball')
        sensor.set_ball({'x': 7, 'y': 1, 'z': 0}, 'axiball')
        sensor.set_ball({'x': 1, 'y': 2, 'z': 0}, 'diagball')
        sensor.ball_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2}  # ball plane normal in global z
        # in Matt frame:
        sensor.set_sensor_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0})

        normal = sensor.get_sensor_normal_pinframe()
        self.assertAlmostEqual(1, normal[0])
        self.assertAlmostEqual(0, normal[1])
        self.assertAlmostEqual(0, normal[2])


if __name__ == '__main__':
    unittest.main()
