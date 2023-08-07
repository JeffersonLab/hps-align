
import unittest
import numpy as np

from hps_align.survey._fixture import Fixture


class TestInit(unittest.TestCase):

    def test_no_input(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        empty_dict = {'x': 0, 'y': 0, 'z': 0}
        empty_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0}
        self.assertEqual(empty_dict, fixture.oriball_dict)
        self.assertEqual(empty_dict, fixture.diagball_dict)
        self.assertEqual(empty_dict, fixture.axiball_dict)
        self.assertEqual(empty_dict, fixture.oripin_dict)
        self.assertEqual(empty_dict, fixture.axipin_dict)
        self.assertEqual(empty_plane_dict, fixture.base_plane_dict)


class TestGetBall(unittest.TestCase):

    def test_invalid_input(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        with self.assertRaises(ValueError):
            fixture.get_ball('foo')

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        empty_array = [0, 0, 0]
        self.assertEqual(empty_array, fixture.get_ball('oriball').tolist())
        self.assertEqual(empty_array, fixture.get_ball('diagball').tolist())
        self.assertEqual(empty_array, fixture.get_ball('axiball').tolist())


class TestSetBall(unittest.TestCase):

    def test_invalid_input(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        with self.assertRaises(ValueError):
            fixture.set_ball('oriball', [0, 0, 0])

        with self.assertRaises(ValueError):
            fixture.set_ball('foo', {'x': 0, 'y': 0, 'z': 0})

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        fixture.set_ball({'x': 1, 'y': 2, 'z': 3}, 'oriball')
        fixture.set_ball({'x': 4, 'y': 5, 'z': 6}, 'diagball')
        fixture.set_ball({'x': 7, 'y': 8, 'z': 9}, 'axiball')

        self.assertEqual([1, 2, 3], fixture.get_ball('oriball').tolist())
        self.assertEqual([4, 5, 6], fixture.get_ball('diagball').tolist())
        self.assertEqual([7, 8, 9], fixture.get_ball('axiball').tolist())


class TestGetBallBasis(unittest.TestCase):

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        fixture.set_ball({'x': 1, 'y': 0, 'z': 0}, 'oriball')
        fixture.set_ball({'x': 1, 'y': 1, 'z': 0}, 'axiball')
        fixture.set_ball({'x': 1, 'y': 0, 'z': 1}, 'diagball')

        basis, origin = fixture.get_ball_basis()
        self.assertEqual([0, 1, 0], basis[0].tolist())
        self.assertEqual([0, 0, 1], basis[1].tolist())
        self.assertEqual([1, 0, 0], basis[2].tolist())
        self.assertEqual([1, 0, 0], origin.tolist())


class TestGetPin(unittest.TestCase):

    def test_invalid_input(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        with self.assertRaises(ValueError):
            fixture.get_pin('foo')

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        empty_array = [0, 0, 0]
        self.assertEqual(empty_array, fixture.get_pin('oripin').tolist())
        self.assertEqual(empty_array, fixture.get_pin('axipin').tolist())


class TestSetPin(unittest.TestCase):

    def test_invalid_input(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        with self.assertRaises(ValueError):
            fixture.set_pin('oripin', [0, 0, 0])

        with self.assertRaises(ValueError):
            fixture.set_pin('foo', {'x': 0, 'y': 0, 'z': 0})

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        fixture.set_pin({'x': 1, 'y': 2, 'z': 3}, 'oripin')
        fixture.set_pin({'x': 4, 'y': 5, 'z': 6}, 'axipin')

        self.assertEqual([1, 2, 3], fixture.get_pin('oripin').tolist())
        self.assertEqual([4, 5, 6], fixture.get_pin('axipin').tolist())


class TestGetBasePlane(unittest.TestCase):

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        plane_origin, plane_normal = fixture.get_base_plane()
        self.assertEqual([0, 0, 0], plane_origin.tolist())
        self.assertEqual([1, 0, 0], plane_normal.tolist())


class TestSetBasePlane(unittest.TestCase):

    def test_invalid_input(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        with self.assertRaises(ValueError):
            fixture.set_base_plane([0, 0, 0])

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        fixture.set_base_plane({'x': 1, 'y': 2, 'z': 3, 'xy_angle': np.pi/2, 'elevation': 0})

        plane_origin, plane_normal = fixture.get_base_plane()
        self.assertEqual([1, 2, 3], plane_origin.tolist())
        self.assertAlmostEqual(0, plane_normal[0])
        self.assertAlmostEqual(1, plane_normal[1])
        self.assertAlmostEqual(0, plane_normal[2])


class TestGetPinBasis(unittest.TestCase):

    def test_invalid_input(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        with self.assertRaises(ValueError):
            fixture.get_pin_basis('foo')

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        fixture.set_pin({'x': 1, 'y': 0, 'z': 1}, 'oripin')
        fixture.set_pin({'x': 1, 'y': 1, 'z': 1}, 'axipin')
        fixture.set_base_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2})

        basis, origin = fixture.get_pin_basis('bottom')
        self.assertAlmostEqual(0, basis[0][0])
        self.assertAlmostEqual(1, basis[0][1])
        self.assertAlmostEqual(0, basis[0][2])
        self.assertAlmostEqual(0, basis[1][0])
        self.assertAlmostEqual(0, basis[1][1])
        self.assertAlmostEqual(1, basis[1][2])
        self.assertAlmostEqual(1, basis[2][0])
        self.assertAlmostEqual(0, basis[2][1])
        self.assertAlmostEqual(0, basis[2][2])
        self.assertAlmostEqual(1, origin[0])
        self.assertAlmostEqual(0, origin[1])
        self.assertAlmostEqual(0, origin[2])

        basis, origin = fixture.get_pin_basis('top')
        self.assertAlmostEqual(0, basis[0][0])
        self.assertAlmostEqual(-1, basis[0][1])
        self.assertAlmostEqual(0, basis[0][2])
        self.assertAlmostEqual(0, basis[1][0])
        self.assertAlmostEqual(0, basis[1][1])
        self.assertAlmostEqual(1, basis[1][2])
        self.assertAlmostEqual(-1, basis[2][0])
        self.assertAlmostEqual(0, basis[2][1])
        self.assertAlmostEqual(0, basis[2][2])
        self.assertAlmostEqual(1, origin[0])
        self.assertAlmostEqual(1, origin[1])
        self.assertAlmostEqual(0, origin[2])


class TestGetPinInBall(unittest.TestCase):

    def test_invalid_input(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        with self.assertRaises(ValueError):
            fixture.get_pin_in_ball('foo')

    def test_matt_coords(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        fixture.set_pin({'x': 1, 'y': 0, 'z': 1}, 'oripin')
        fixture.set_pin({'x': 1, 'y': 1, 'z': 1}, 'axipin')
        fixture.set_base_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2})

        basis, origin = fixture.get_pin_in_ball('bottom', True)
        self.assertAlmostEqual(0, basis[0][0])
        self.assertAlmostEqual(1, basis[0][1])
        self.assertAlmostEqual(0, basis[0][2])
        self.assertAlmostEqual(0, basis[1][0])
        self.assertAlmostEqual(0, basis[1][1])
        self.assertAlmostEqual(1, basis[1][2])
        self.assertAlmostEqual(1, basis[2][0])
        self.assertAlmostEqual(0, basis[2][1])
        self.assertAlmostEqual(0, basis[2][2])
        self.assertAlmostEqual(1, origin[0])
        self.assertAlmostEqual(0, origin[1])
        self.assertAlmostEqual(0, origin[2])

        basis, origin = fixture.get_pin_in_ball('top', True)
        self.assertAlmostEqual(0, basis[0][0])
        self.assertAlmostEqual(-1, basis[0][1])
        self.assertAlmostEqual(0, basis[0][2])
        self.assertAlmostEqual(0, basis[1][0])
        self.assertAlmostEqual(0, basis[1][1])
        self.assertAlmostEqual(1, basis[1][2])
        self.assertAlmostEqual(-1, basis[2][0])
        self.assertAlmostEqual(0, basis[2][1])
        self.assertAlmostEqual(0, basis[2][2])
        self.assertAlmostEqual(1, origin[0])
        self.assertAlmostEqual(1, origin[1])
        self.assertAlmostEqual(0, origin[2])

    def test_generic_coords(self):
        with self.assertWarns(UserWarning):
            fixture = Fixture()

        fixture.set_pin({'x': 1, 'y': 0, 'z': 1}, 'oripin')
        fixture.set_pin({'x': 1, 'y': 1, 'z': 1}, 'axipin')
        fixture.set_base_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2})
        fixture.set_ball({'x': 0, 'y': 0, 'z': 0}, 'oriball')
        fixture.set_ball({'x': -1, 'y': 0, 'z': 0}, 'axiball')
        fixture.set_ball({'x': 0, 'y': -1, 'z': 0}, 'diagball')

        basis, origin = fixture.get_pin_in_ball('bottom')
        self.assertAlmostEqual(0, basis[0][0])
        self.assertAlmostEqual(-1, basis[0][1])
        self.assertAlmostEqual(0, basis[0][2])
        self.assertAlmostEqual(0, basis[1][0])
        self.assertAlmostEqual(0, basis[1][1])
        self.assertAlmostEqual(-1, basis[1][2])
        self.assertAlmostEqual(1, basis[2][0])
        self.assertAlmostEqual(0, basis[2][1])
        self.assertAlmostEqual(0, basis[2][2])
        self.assertAlmostEqual(-1, origin[0])
        self.assertAlmostEqual(0, origin[1])
        self.assertAlmostEqual(0, origin[2])

        basis, origin = fixture.get_pin_in_ball('top')
        self.assertAlmostEqual(0, basis[0][0])
        self.assertAlmostEqual(1, basis[0][1])
        self.assertAlmostEqual(0, basis[0][2])
        self.assertAlmostEqual(0, basis[1][0])
        self.assertAlmostEqual(0, basis[1][1])
        self.assertAlmostEqual(-1, basis[1][2])
        self.assertAlmostEqual(-1, basis[2][0])
        self.assertAlmostEqual(0, basis[2][1])
        self.assertAlmostEqual(0, basis[2][2])
        self.assertAlmostEqual(-1, origin[0])
        self.assertAlmostEqual(-1, origin[1])
        self.assertAlmostEqual(0, origin[2])

    # def test_input_file(self):
    #     fixture = Fixture('/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L0_fixture_empty_1.txt')

    #     basis_bot, origin_bot = fixture.get_pin_in_ball('bottom', True)
    #     basis_top, origin_top = fixture.get_pin_in_ball('top', True)

    #     print('bottom origin: ', origin_bot)
    #     print('top origin: ', origin_top)
    #     print('axipin:', fixture.get_pin('axipin'))
    #     print('oripin:', fixture.get_pin('oripin'))


if __name__ == '__main__':
    unittest.main()