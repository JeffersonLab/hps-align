
import unittest
import numpy as np

from hps_align.survey._sensors import Sensor


class TestInit(unittest.TestCase):

    def test_no_input(self):
        with self.assertWarns(UserWarning):
            sensor = Sensor()

        empty_dict = {'x': 0, 'y': 0, 'z': 0}
        empty_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0}
        self.assertEqual(empty_dict, sensor.oriball_dict)
        self.assertEqual(empty_dict, sensor.diagball_dict)
        self.assertEqual(empty_dict, sensor.axiball_dict)
        self.assertEqual(empty_dict, sensor.sensor_origin_dict)
        self.assertEqual(empty_plane_dict, sensor.sensor_plane_dict)
        self.assertEqual(empty_dict, sensor.fixture.oriball_dict)
        self.assertEqual(empty_dict, sensor.fixture.diagball_dict)
        self.assertEqual(empty_dict, sensor.fixture.axiball_dict)
        self.assertEqual(empty_dict, sensor.fixture.oripin_dict)
        self.assertEqual(empty_dict, sensor.fixture.axipin_dict)
        self.assertEqual(empty_plane_dict, sensor.fixture.base_plane_dict)


class TestGetBall(unittest.TestCase):

    def test_invalid_input(self):
        with self.assertWarns(UserWarning):
            sensor = Sensor()

        with self.assertRaises(ValueError):
            sensor.get_ball('foo')

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            sensor = Sensor()

        empty_array = [0, 0, 0]
        self.assertEqual(empty_array, sensor.get_ball('oriball').tolist())
        self.assertEqual(empty_array, sensor.get_ball('diagball').tolist())
        self.assertEqual(empty_array, sensor.get_ball('axiball').tolist())


class TestSetBall(unittest.TestCase):

    def test_invalid_input(self):
        with self.assertWarns(UserWarning):
            sensor = Sensor()

        with self.assertRaises(ValueError):
            sensor.set_ball('oriball', [0, 0, 0])

        with self.assertRaises(ValueError):
            sensor.set_ball('foo', {'x': 0, 'y': 0, 'z': 0})

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            sensor = Sensor()

        sensor.set_ball({'x': 1, 'y': 2, 'z': 3}, 'oriball')
        sensor.set_ball({'x': 4, 'y': 5, 'z': 6}, 'diagball')
        sensor.set_ball({'x': 7, 'y': 8, 'z': 9}, 'axiball')

        self.assertEqual([1, 2, 3], sensor.get_ball('oriball').tolist())
        self.assertEqual([4, 5, 6], sensor.get_ball('diagball').tolist())
        self.assertEqual([7, 8, 9], sensor.get_ball('axiball').tolist())


class TestGetBallBasis(unittest.TestCase):

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            sensor = Sensor()

        sensor.set_ball({'x': 1, 'y': 0, 'z': 0}, 'oriball')
        sensor.set_ball({'x': 1, 'y': 1, 'z': 0}, 'axiball')
        sensor.set_ball({'x': 1, 'y': 0, 'z': 1}, 'diagball')

        basis, origin = sensor.get_ball_basis()
        self.assertEqual([0, 1, 0], basis[0].tolist())
        self.assertEqual([0, 0, 1], basis[1].tolist())
        self.assertEqual([1, 0, 0], basis[2].tolist())
        self.assertEqual([1, 0, 0], origin.tolist())


class TestSensorOrigin(unittest.TestCase):

    def test_get_origin(self):
        with self.assertWarns(UserWarning):
            sensor = Sensor()

        self.assertEqual([0, 0, 0], sensor.get_sensor_origin().tolist())

    def test_set_origin_invalid_input(self):
        with self.assertWarns(UserWarning):
            sensor = Sensor()

        with self.assertRaises(ValueError):
            sensor.set_sensor_origin([0, 0, 0])

    def test_set_origin_valid_input(self):
        with self.assertWarns(UserWarning):
            sensor = Sensor()

        sensor.set_sensor_origin({'x': 1, 'y': 2, 'z': 3})
        self.assertEqual([1, 2, 3], sensor.get_sensor_origin().tolist())

    def test_get_sensor_origin_ballframe(self):
        with self.assertWarns(UserWarning):
            sensor = Sensor()

        sensor.set_ball({'x': 1, 'y': 0, 'z': 0}, 'oriball')
        sensor.set_ball({'x': 1, 'y': 1, 'z': 0}, 'axiball')
        sensor.set_ball({'x': 1, 'y': 0, 'z': 1}, 'diagball')
        sensor.set_sensor_origin({'x': 1, 'y': 2, 'z': 3})

        self.assertEqual([1, 2, 3], sensor.get_sensor_origin_ballframe(True).tolist())
        self.assertEqual([2, 3, 0], sensor.get_sensor_origin_ballframe(False).tolist())

    def test_get_sensor_origin_pinframe(self):
        with self.assertWarns(UserWarning):
            sensor = Sensor()

        sensor.set_ball({'x': 1, 'y': 0, 'z': 0}, 'oriball')
        sensor.set_ball({'x': 1, 'y': 1, 'z': 0}, 'axiball')
        sensor.set_ball({'x': 1, 'y': 0, 'z': 1}, 'diagball')
        sensor.set_sensor_origin({'x': 1, 'y': 2, 'z': 3})

        sensor.fixture.set_ball({'x': 1, 'y': 0, 'z': 0}, 'oriball')
        sensor.fixture.set_ball({'x': 1, 'y': 1, 'z': 0}, 'axiball')
        sensor.fixture.set_ball({'x': 1, 'y': 0, 'z': 1}, 'diagball')
        sensor.fixture.set_pin({'x': 1, 'y': 0, 'z': 1}, 'oripin')
        sensor.fixture.set_pin({'x': 1, 'y': 1, 'z': 1}, 'axipin')
        sensor.fixture.set_base_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2})

        self.assertAlmostEqual(-1, sensor.get_sensor_origin_pinframe('top', True)[0])
        self.assertAlmostEqual(3, sensor.get_sensor_origin_pinframe('top', True)[1])
        self.assertAlmostEqual(0, sensor.get_sensor_origin_pinframe('top', True)[2])

        self.assertAlmostEqual(2, sensor.get_sensor_origin_pinframe('bottom', True)[0])
        self.assertAlmostEqual(3, sensor.get_sensor_origin_pinframe('bottom', True)[1])
        self.assertAlmostEqual(0, sensor.get_sensor_origin_pinframe('bottom', True)[2])


class TestSensorNormal(unittest.TestCase):

    def test_get_normal(self):
        with self.assertWarns(UserWarning):
            sensor = Sensor()

        self.assertEqual([1, 0, 0], sensor.get_sensor_normal().tolist())

    def test_set_sensor_plane(self):
        with self.assertWarns(UserWarning):
            sensor = Sensor()

        sensor.set_sensor_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2})
        self.assertAlmostEqual(0, sensor.get_sensor_normal()[0])
        self.assertAlmostEqual(0, sensor.get_sensor_normal()[1])
        self.assertAlmostEqual(1, sensor.get_sensor_normal()[2])

    def test_get_sensor_normal_ballframe(self):
        with self.assertWarns(UserWarning):
            sensor = Sensor()

        sensor.set_ball({'x': 1, 'y': 0, 'z': 0}, 'oriball')
        sensor.set_ball({'x': 1, 'y': 1, 'z': 0}, 'axiball')
        sensor.set_ball({'x': 1, 'y': 0, 'z': 1}, 'diagball')
        sensor.set_sensor_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2})

        self.assertAlmostEqual(0, sensor.get_sensor_normal_ballframe(True)[0])
        self.assertAlmostEqual(0, sensor.get_sensor_normal_ballframe(True)[1])
        self.assertAlmostEqual(1, sensor.get_sensor_normal_ballframe(True)[2])

        self.assertAlmostEqual(0, sensor.get_sensor_normal_ballframe(False)[0])
        self.assertAlmostEqual(1, sensor.get_sensor_normal_ballframe(False)[1])
        self.assertAlmostEqual(0, sensor.get_sensor_normal_ballframe(False)[2])

    def test_get_sensor_normal_pinframe(self):
        with self.assertWarns(UserWarning):
            sensor = Sensor()

        sensor.set_ball({'x': 1, 'y': 0, 'z': 0}, 'oriball')
        sensor.set_ball({'x': 1, 'y': 1, 'z': 0}, 'axiball')
        sensor.set_ball({'x': 1, 'y': 0, 'z': 1}, 'diagball')
        sensor.set_sensor_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2})

        sensor.fixture.set_ball({'x': 1, 'y': 0, 'z': 0}, 'oriball')
        sensor.fixture.set_ball({'x': 1, 'y': 1, 'z': 0}, 'axiball')
        sensor.fixture.set_ball({'x': 1, 'y': 0, 'z': 1}, 'diagball')
        sensor.fixture.set_pin({'x': 1, 'y': 0, 'z': 1}, 'oripin')
        sensor.fixture.set_pin({'x': 1, 'y': 1, 'z': 1}, 'axipin')
        sensor.fixture.set_base_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2})

        self.assertAlmostEqual(0, sensor.get_sensor_normal_pinframe('top', True)[0])
        self.assertAlmostEqual(1, sensor.get_sensor_normal_pinframe('top', True)[1])
        self.assertAlmostEqual(0, sensor.get_sensor_normal_pinframe('top', True)[2])

        self.assertAlmostEqual(0, sensor.get_sensor_normal_pinframe('bottom', True)[0])
        self.assertAlmostEqual(1, sensor.get_sensor_normal_pinframe('bottom', True)[1])
        self.assertAlmostEqual(0, sensor.get_sensor_normal_pinframe('bottom', True)[2])

    # def test_input_file(self):
    #     sensor = Sensor('/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L0_axial1_1.txt',
    #                     '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L0_fixture_empty_1.txt')

    #     origin_bot = sensor.get_sensor_origin_pinframe('bottom', True)
    #     origin_top = sensor.get_sensor_origin_pinframe('top', True)

    #     print('bottom origin: ', origin_bot)
    #     print('top origin: ', origin_top)


if __name__ == '__main__':
    unittest.main()
