
import unittest
import numpy as np

from hps_align.survey._pinframe import PinFrame
from hps_align.survey._pins import Pin
from hps_align.survey._baseplanes import BasePlane


class TestInit(unittest.TestCase):

    def test_no_input(self):
        with self.assertWarns(UserWarning):
            pinframe = PinFrame()

        empty_pin_dict = {'x': 0, 'y': 0, 'z': 0}
        self.assertEqual(empty_pin_dict, pinframe.pins.L0_hole_pin_dict)
        self.assertEqual(empty_pin_dict, pinframe.pins.L0_slot_pin_dict)
        self.assertEqual(empty_pin_dict, pinframe.pins.L1_hole_pin_dict)
        self.assertEqual(empty_pin_dict, pinframe.pins.L1_slot_pin_dict)
        self.assertEqual(empty_pin_dict, pinframe.pins.L2_hole_pin_dict)
        self.assertEqual(empty_pin_dict, pinframe.pins.L2_slot_pin_dict)
        self.assertEqual(empty_pin_dict, pinframe.pins.L3_hole_pin_dict)
        self.assertEqual(empty_pin_dict, pinframe.pins.L3_slot_pin_dict)

        empty_base_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0}
        self.assertEqual(empty_base_dict, pinframe.base_planes.L0_base_plane_dict)
        self.assertEqual(empty_base_dict, pinframe.base_planes.L1_base_plane_dict)
        self.assertEqual(empty_base_dict, pinframe.base_planes.L2_base_plane_dict)
        self.assertEqual(empty_base_dict, pinframe.base_planes.L3_base_plane_dict)


class TestGetBasis(unittest.TestCase):

    def test_invalid_input(self):
        with self.assertWarns(UserWarning):
            pinframe = PinFrame()

        with self.assertRaises(ValueError):
            pinframe.get_basis(4)

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            pinframe = PinFrame()

        with self.assertWarns(UserWarning):
            pin = Pin()

        pin.set_pin({'x': 0, 'y': 0, 'z': 0}, 0, 'hole')
        pin.set_pin({'x': 1, 'y': 0, 'z': 0}, 0, 'slot')

        with self.assertWarns(UserWarning):
            baseplane = BasePlane()

        baseplane.set_base_plane_dict({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2}, 0)

        pinframe.pins = pin
        pinframe.base_planes = baseplane
        basis, origin = pinframe.get_basis(0)

        self.assertEqual([0, 0, 0], origin.tolist())
        self.assertAlmostEqual(-1, basis[0][0])
        self.assertAlmostEqual(0, basis[0][1])
        self.assertAlmostEqual(0, basis[0][2])
        self.assertAlmostEqual(0, basis[1][0])
        self.assertAlmostEqual(0, basis[1][1])
        self.assertAlmostEqual(1, basis[1][2])
        self.assertAlmostEqual(0, basis[2][0])
        self.assertAlmostEqual(1, basis[2][1])
        self.assertAlmostEqual(0, basis[2][2])

        pin.set_pin({'x': 1, 'y': 0, 'z': -2}, 0, 'hole')
        pin.set_pin({'x': 1, 'y': 1, 'z': 3}, 0, 'slot')

        with self.assertWarns(UserWarning):
            baseplane = BasePlane()

        baseplane.set_base_plane_dict({'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': np.pi/2}, 0)

        pinframe.pins = pin
        pinframe.base_planes = baseplane
        basis, origin = pinframe.get_basis(0)

        self.assertAlmostEqual(1, origin.tolist()[0])
        self.assertAlmostEqual(0, origin.tolist()[1])
        self.assertAlmostEqual(0, origin.tolist()[2])
        self.assertAlmostEqual(0, basis[0][0])
        self.assertAlmostEqual(-1, basis[0][1])
        self.assertAlmostEqual(0, basis[0][2])
        self.assertAlmostEqual(0, basis[1][0])
        self.assertAlmostEqual(0, basis[1][1])
        self.assertAlmostEqual(1, basis[1][2])
        self.assertAlmostEqual(-1, basis[2][0])
        self.assertAlmostEqual(0, basis[2][1])
        self.assertAlmostEqual(0, basis[2][2])


if __name__ == '__main__':
    unittest.main()
