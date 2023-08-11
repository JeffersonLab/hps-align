
import unittest
import numpy as np

from hps_align.survey._uchannel import UChannel
from hps_align.survey._baseplanes import BasePlane
from hps_align.survey._pins import Pin
from hps_align.survey._pinframe import PinFrame
from hps_align.survey._ballframe import BallFrame


class TestInit(unittest.TestCase):

    def test_no_input(self):
        uchannel = UChannel()

        empty_dict_point = {'x': 0, 'y': 0, 'z': 0}
        empty_dict_plane = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0}

        self.assertEqual(empty_dict_plane, uchannel.pinframe_top.base_planes.L0_base_plane_dict)
        self.assertEqual(empty_dict_plane, uchannel.pinframe_top.base_planes.L1_base_plane_dict)
        self.assertEqual(empty_dict_plane, uchannel.pinframe_top.base_planes.L2_base_plane_dict)
        self.assertEqual(empty_dict_plane, uchannel.pinframe_top.base_planes.L3_base_plane_dict)
        self.assertEqual(empty_dict_plane, uchannel.pinframe_bot.base_planes.L0_base_plane_dict)
        self.assertEqual(empty_dict_plane, uchannel.pinframe_bot.base_planes.L1_base_plane_dict)
        self.assertEqual(empty_dict_plane, uchannel.pinframe_bot.base_planes.L2_base_plane_dict)
        self.assertEqual(empty_dict_plane, uchannel.pinframe_bot.base_planes.L3_base_plane_dict)

        self.assertEqual(empty_dict_point, uchannel.pinframe_top.pins.L0_hole_pin_dict)
        self.assertEqual(empty_dict_point, uchannel.pinframe_top.pins.L0_slot_pin_dict)
        self.assertEqual(empty_dict_point, uchannel.pinframe_top.pins.L1_hole_pin_dict)
        self.assertEqual(empty_dict_point, uchannel.pinframe_top.pins.L1_slot_pin_dict)
        self.assertEqual(empty_dict_point, uchannel.pinframe_top.pins.L2_hole_pin_dict)
        self.assertEqual(empty_dict_point, uchannel.pinframe_top.pins.L2_slot_pin_dict)
        self.assertEqual(empty_dict_point, uchannel.pinframe_top.pins.L3_hole_pin_dict)
        self.assertEqual(empty_dict_point, uchannel.pinframe_top.pins.L3_slot_pin_dict)
        self.assertEqual(empty_dict_point, uchannel.pinframe_bot.pins.L0_hole_pin_dict)
        self.assertEqual(empty_dict_point, uchannel.pinframe_bot.pins.L0_slot_pin_dict)
        self.assertEqual(empty_dict_point, uchannel.pinframe_bot.pins.L1_hole_pin_dict)
        self.assertEqual(empty_dict_point, uchannel.pinframe_bot.pins.L1_slot_pin_dict)
        self.assertEqual(empty_dict_point, uchannel.pinframe_bot.pins.L2_hole_pin_dict)
        self.assertEqual(empty_dict_point, uchannel.pinframe_bot.pins.L2_slot_pin_dict)
        self.assertEqual(empty_dict_point, uchannel.pinframe_bot.pins.L3_hole_pin_dict)
        self.assertEqual(empty_dict_point, uchannel.pinframe_bot.pins.L3_slot_pin_dict)

        self.assertEqual(empty_dict_point, uchannel.ballframe_top.L1_hole_ball_dict)
        self.assertEqual(empty_dict_point, uchannel.ballframe_top.L1_slot_ball_dict)
        self.assertEqual(empty_dict_point, uchannel.ballframe_top.L3_hole_ball_dict)
        self.assertEqual(empty_dict_point, uchannel.ballframe_top.L3_slot_ball_dict)
        self.assertEqual(empty_dict_point, uchannel.ballframe_bot.L1_hole_ball_dict)
        self.assertEqual(empty_dict_point, uchannel.ballframe_bot.L1_slot_ball_dict)
        self.assertEqual(empty_dict_point, uchannel.ballframe_bot.L3_hole_ball_dict)
        self.assertEqual(empty_dict_point, uchannel.ballframe_bot.L3_slot_ball_dict)


class TestGetBallBasis(unittest.TestCase):

    def test_invalid_input(self):
        uchannel = UChannel()

        with self.assertRaises(ValueError):
            uchannel.get_ball_basis('foo')

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            ballframe = BallFrame()
            ballframe.set_ball({'x': 2, 'y': 0, 'z': 0}, 1, 'hole')
            ballframe.set_ball({'x': 0, 'y': 0, 'z': 0}, 1, 'slot')
            ballframe.set_ball({'x': 2, 'y': 6, 'z': 0}, 3, 'hole')
            ballframe.set_ball({'x': 0, 'y': 6, 'z': 0}, 3, 'slot')

        uchannel = UChannel(ballframe_top=ballframe)

        basis, origin = uchannel.get_ball_basis('top')

        self.assertEqual([0, 0, 0], origin.tolist())
        self.assertEqual([-1, 0, 0], basis[0].tolist())
        self.assertEqual([0, 0, 1], basis[1].tolist())
        self.assertEqual([0, 1, 0], basis[2].tolist())


class TestGetPinBasis(unittest.TestCase):

    def test_invalid_input(self):
        uchannel = UChannel()

        with self.assertRaises(ValueError):
            uchannel.get_pin_basis(1, 'foo')

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            pin = Pin()

            pin.set_pin({'x': 0, 'y': 0, 'z': 0}, 0, 'hole')
            pin.set_pin({'x': 1, 'y': 0, 'z': 0}, 0, 'slot')

        with self.assertWarns(UserWarning):
            baseplane = BasePlane()

            baseplane.set_base_plane_dict({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2}, 0)

        with self.assertWarns(UserWarning):
            pinframe = PinFrame()
            pinframe.pins = pin
            pinframe.base_planes = baseplane
            # gives pin_basis [[1, 0, 0], [0, 0, 1], [0, -1, 0]]

        uchannel = UChannel(pinframe_top=pinframe)

        basis, origin = uchannel.get_pin_basis(0, 'top')

        self.assertEqual([0, 0, 0], origin.tolist())
        self.assertAlmostEqual(1, basis[0][0])
        self.assertAlmostEqual(0, basis[0][1])
        self.assertAlmostEqual(0, basis[0][2])
        self.assertAlmostEqual(0, basis[1][0])
        self.assertAlmostEqual(0, basis[1][1])
        self.assertAlmostEqual(1, basis[1][2])
        self.assertAlmostEqual(0, basis[2][0])
        self.assertAlmostEqual(-1, basis[2][1])
        self.assertAlmostEqual(0, basis[2][2])


class TestPinToBallFrame(unittest.TestCase):

    def test_valid_input(self):

        with self.assertWarns(UserWarning):
            pin = Pin()
            pin.set_pin({'x': 0, 'y': 0, 'z': 0}, 0, 'hole')
            pin.set_pin({'x': 1, 'y': 0, 'z': 0}, 0, 'slot')

        with self.assertWarns(UserWarning):
            baseplane = BasePlane()
            baseplane.set_base_plane_dict({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2}, 0)

        with self.assertWarns(UserWarning):
            pinframe = PinFrame()
            pinframe.pins = pin
            pinframe.base_planes = baseplane
            # uchannel.pinframe_top = pinframe
            # gives pin_basis [[1, 0, 0], [0, 0, 1], [0, -1, 0]]

        with self.assertWarns(UserWarning):
            ballframe = BallFrame()
            ballframe.set_ball({'x': 2, 'y': 0, 'z': 0}, 1, 'hole')
            ballframe.set_ball({'x': 0, 'y': 0, 'z': 0}, 1, 'slot')
            ballframe.set_ball({'x': 2, 'y': 6, 'z': 0}, 3, 'hole')
            ballframe.set_ball({'x': 0, 'y': 6, 'z': 0}, 3, 'slot')
            # uchannel.ballframe_top = ballframe
            # gives ball_basis [[-1, 0, 0], [0, 0, 1], [0, 1, 0]]

        uchannel = UChannel(pinframe_top=pinframe, ballframe_top=ballframe)

        basis, origin = uchannel.pin_in_ballframe(0, 'top')

        self.assertEqual([0, 0, 0], origin.tolist())
        self.assertAlmostEqual(-1, basis[0][0])
        self.assertAlmostEqual(0, basis[0][1])
        self.assertAlmostEqual(0, basis[0][2])
        self.assertAlmostEqual(0, basis[1][0])
        self.assertAlmostEqual(-1, basis[1][1])
        self.assertAlmostEqual(0, basis[1][2])
        self.assertAlmostEqual(0, basis[2][0])
        self.assertAlmostEqual(0, basis[2][1])
        self.assertAlmostEqual(1, basis[2][2])

    def test_valid_input_top(self):
        with self.assertWarns(UserWarning):
            pin = Pin()

            pin.set_pin({'x': 1, 'y': 2, 'z': 0}, 0, 'hole')
            pin.set_pin({'x': 2, 'y': 2, 'z': 0}, 0, 'slot')

        with self.assertWarns(UserWarning):
            baseplane = BasePlane()

            baseplane.set_base_plane_dict({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2}, 0)

        with self.assertWarns(UserWarning):
            pinframe = PinFrame()
            pinframe.pins = pin
            pinframe.base_planes = baseplane
            # gives pin_basis [[1, 0, 0], [0, 0, 1], [0, -1, 0]]

        with self.assertWarns(UserWarning):
            ballframe = BallFrame()
            ballframe.set_ball({'x': 0, 'y': 1, 'z': 0}, 1, 'hole')
            ballframe.set_ball({'x': 3, 'y': 1, 'z': 0}, 1, 'slot')
            ballframe.set_ball({'x': 0, 'y': 4, 'z': 0}, 3, 'hole')
            ballframe.set_ball({'x': 3, 'y': 4, 'z': 0}, 3, 'slot')
            # gives ball_basis [[1, 0, 0], [0, 0, -1], [0, 1, 0]]

        uchannel = UChannel(pinframe_top=pinframe, ballframe_top=ballframe)
        basis, origin = uchannel.pin_in_ballframe(0, 'top')

        self.assertAlmostEqual(-2, origin[0])
        self.assertAlmostEqual(0, origin[1])
        self.assertAlmostEqual(1, origin[2])
        self.assertAlmostEqual(1, basis[0][0])
        self.assertAlmostEqual(0, basis[0][1])
        self.assertAlmostEqual(0, basis[0][2])
        self.assertAlmostEqual(0, basis[1][0])
        self.assertAlmostEqual(-1, basis[1][1])
        self.assertAlmostEqual(0, basis[1][2])
        self.assertAlmostEqual(0, basis[2][0])
        self.assertAlmostEqual(0, basis[2][1])
        self.assertAlmostEqual(-1, basis[2][2])

    def test_valid_input_bot(self):
        with self.assertWarns(UserWarning):
            pin = Pin()

            pin.set_pin({'x': 1, 'y': 2, 'z': 0}, 0, 'slot')
            pin.set_pin({'x': 2, 'y': 2, 'z': 0}, 0, 'hole')

        with self.assertWarns(UserWarning):
            baseplane = BasePlane()

            baseplane.set_base_plane_dict({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2}, 0)

        with self.assertWarns(UserWarning):
            pinframe = PinFrame()
            pinframe.pins = pin
            pinframe.base_planes = baseplane
            # gives pin_basis [[-1, 0, 0], [0, 0, 1], [0, 1, 0]]

        with self.assertWarns(UserWarning):
            ballframe = BallFrame()
            ballframe.set_ball({'x': 0, 'y': 1, 'z': 0}, 1, 'slot')
            ballframe.set_ball({'x': 3, 'y': 1, 'z': 0}, 1, 'hole')
            ballframe.set_ball({'x': 0, 'y': 4, 'z': 0}, 3, 'slot')
            ballframe.set_ball({'x': 3, 'y': 4, 'z': 0}, 3, 'hole')
            # gives ball_basis [[-1, 0, 0], [0, 0, 1], [0, 1, 0]]

        uchannel = UChannel(pinframe_bot=pinframe, ballframe_bot=ballframe)
        basis, origin = uchannel.pin_in_ballframe(0, 'bottom')

        self.assertAlmostEqual(-2, origin[0])
        self.assertAlmostEqual(0, origin[1])
        self.assertAlmostEqual(1, origin[2])
        self.assertAlmostEqual(1, basis[0][0])
        self.assertAlmostEqual(0, basis[0][1])
        self.assertAlmostEqual(0, basis[0][2])
        self.assertAlmostEqual(0, basis[1][0])
        self.assertAlmostEqual(1, basis[1][1])
        self.assertAlmostEqual(0, basis[1][2])
        self.assertAlmostEqual(0, basis[2][0])
        self.assertAlmostEqual(0, basis[2][1])
        self.assertAlmostEqual(1, basis[2][2])

    # def test_txt_input(self):
    #     input_files = {'top': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_empty_top_1.txt',
    #                      'bottom': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_empty_bottom_1.txt'}

    #     ballframe_top = BallFrame(input_files['top'])
    #     ballframe_bot = BallFrame(input_files['bottom'])
    #     pinframe_top = PinFrame(input_files['top'])
    #     pinframe_bot = PinFrame(input_files['bottom'])
    #     uchannel = UChannel(ballframe_top=ballframe_top, ballframe_bot=ballframe_bot, pinframe_top=pinframe_top, pinframe_bot=pinframe_bot)

    #     print('top')
    #     print(uchannel.pin_in_ballframe(0, 'top', True)[1])
    #     print(uchannel.pin_in_ballframe(1, 'top', True)[1])
    #     print(uchannel.pin_in_ballframe(2, 'top', True)[1])
    #     print(uchannel.pin_in_ballframe(3, 'top', True)[1])
    #     print('bottom')
    #     print(uchannel.pin_in_ballframe(0, 'bottom', True)[1])
    #     print(uchannel.pin_in_ballframe(1, 'bottom', True)[1])
    #     print(uchannel.pin_in_ballframe(2, 'bottom', True)[1])
    #     print(uchannel.pin_in_ballframe(3, 'bottom', True)[1])


if __name__ == '__main__':
    unittest.main()
