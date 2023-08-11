
import unittest
import numpy as np

from hps_align.survey._fixture import MattFixture


class TestInit(unittest.TestCase):

    def test_no_input(self):
        with self.assertWarns(UserWarning):
            fixture = MattFixture()

        empty_dict = {'x': 0, 'y': 0, 'z': 0}
        empty_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0}
        self.assertEqual(empty_dict, fixture.oriball_dict)
        self.assertEqual(empty_dict, fixture.diagball_dict)
        self.assertEqual(empty_dict, fixture.axiball_dict)
        self.assertEqual(empty_dict, fixture.oripin_dict)
        self.assertEqual(empty_dict, fixture.axipin_dict)
        self.assertEqual(empty_plane_dict, fixture.base_plane_dict)


class TestGetBallBasis(unittest.TestCase):

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            fixture = MattFixture()

        fixture.set_ball({'x': 1, 'y': 0, 'z': 0}, 'oriball')
        fixture.set_ball({'x': 1, 'y': 1, 'z': 0}, 'axiball')
        fixture.set_ball({'x': 1, 'y': 0, 'z': 1}, 'diagball')

        basis, origin = fixture.get_ball_basis()
        self.assertEqual([0, 1, 0], basis[0].tolist())
        self.assertEqual([0, 0, 1], basis[1].tolist())
        self.assertEqual([1, 0, 0], basis[2].tolist())
        self.assertEqual([1, 0, 0], origin.tolist())


class TestGetPinBasis(unittest.TestCase):

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            fixture = MattFixture()

        fixture.set_pin({'x': 1, 'y': 0, 'z': 1}, 'oripin')
        fixture.set_pin({'x': 1, 'y': 1, 'z': 1}, 'axipin')
        fixture.set_base_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2})

        basis, origin = fixture.get_pin_basis()
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


class TestGetNestedCoords(unittest.TestCase):

    def test_pin_in_ball(self):
        with self.assertWarns(UserWarning):
            fixture = MattFixture()

        fixture.set_pin({'x': 1, 'y': 0, 'z': 1}, 'oripin')
        fixture.set_pin({'x': 1, 'y': 1, 'z': 1}, 'axipin')
        fixture.set_base_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2})
        fixture.set_ball({'x': 0, 'y': 0, 'z': 0}, 'oriball')
        fixture.set_ball({'x': -5, 'y': 0, 'z': 0}, 'axiball')
        fixture.set_ball({'x': 0, 'y': -2, 'z': 0}, 'diagball')

        basis, origin = fixture.get_pin_in_ball()
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

    def test_ball_in_pin(self):
        with self.assertWarns(UserWarning):
            fixture = MattFixture()

        fixture.set_pin({'x': 1, 'y': 0, 'z': 1}, 'oripin')
        fixture.set_pin({'x': 1, 'y': 1, 'z': 1}, 'axipin')
        fixture.set_base_plane({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2})
        fixture.set_ball({'x': 0, 'y': 0, 'z': 0}, 'oriball')
        fixture.set_ball({'x': -5, 'y': 0, 'z': 0}, 'axiball')
        fixture.set_ball({'x': 0, 'y': -2, 'z': 0}, 'diagball')

        basis, origin = fixture.get_ball_in_pin()
        self.assertAlmostEqual(0, basis[0][0])
        self.assertAlmostEqual(0, basis[0][1])
        self.assertAlmostEqual(-1, basis[0][2])
        self.assertAlmostEqual(-1, basis[1][0])
        self.assertAlmostEqual(0, basis[1][1])
        self.assertAlmostEqual(0, basis[1][2])
        self.assertAlmostEqual(0, basis[2][0])
        self.assertAlmostEqual(1, basis[2][1])
        self.assertAlmostEqual(0, basis[2][2])
        self.assertAlmostEqual(1, origin[0])
        self.assertAlmostEqual(0, origin[1])
        self.assertAlmostEqual(1, origin[2])

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
