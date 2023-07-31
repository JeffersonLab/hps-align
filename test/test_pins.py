
import unittest

from hps_align.survey._pins import Pin


class TestInit(unittest.TestCase):

    def test_no_input(self):
        with self.assertWarns(UserWarning):
            pin = Pin()

        empty_dict = {'x': 0, 'y': 0, 'z': 0}
        self.assertEqual(empty_dict, pin.L0_hole_pin_dict)
        self.assertEqual(empty_dict, pin.L0_slot_pin_dict)
        self.assertEqual(empty_dict, pin.L1_hole_pin_dict)
        self.assertEqual(empty_dict, pin.L1_slot_pin_dict)
        self.assertEqual(empty_dict, pin.L2_hole_pin_dict)
        self.assertEqual(empty_dict, pin.L2_slot_pin_dict)
        self.assertEqual(empty_dict, pin.L3_hole_pin_dict)
        self.assertEqual(empty_dict, pin.L3_slot_pin_dict)


class TestGetPin(unittest.TestCase):

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            pin = Pin()

        self.assertEqual(pin.get_pin(0, 'hole').tolist(), [0.0, 0.0, 0.0])
        self.assertEqual(pin.get_pin(0, 'slot').tolist(), [0.0, 0.0, 0.0])
        self.assertEqual(pin.get_pin(1, 'hole').tolist(), [0.0, 0.0, 0.0])
        self.assertEqual(pin.get_pin(1, 'slot').tolist(), [0.0, 0.0, 0.0])
        self.assertEqual(pin.get_pin(2, 'hole').tolist(), [0.0, 0.0, 0.0])
        self.assertEqual(pin.get_pin(2, 'slot').tolist(), [0.0, 0.0, 0.0])
        self.assertEqual(pin.get_pin(3, 'hole').tolist(), [0.0, 0.0, 0.0])
        self.assertEqual(pin.get_pin(3, 'slot').tolist(), [0.0, 0.0, 0.0])

    def test_invalid_input(self):
        with self.assertWarns(UserWarning):
            pin = Pin()

        with self.assertRaises(ValueError):
            pin.get_pin(4, 'hole')

        with self.assertRaises(ValueError):
            pin.get_pin(3, 'foo')


class TestSetPin(unittest.TestCase):

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            pin = Pin()

        pin.set_pin({'x': 1, 'y': 2, 'z': 0}, 0, 'hole')
        pin.set_pin({'x': 1, 'y': 0, 'z': 0.2}, 0, 'slot')
        pin.set_pin({'x': 5, 'y': 3, 'z': -10}, 1, 'hole')
        pin.set_pin({'x': 0, 'y': 1, 'z': 3}, 1, 'slot')
        pin.set_pin({'x': -9, 'y': 0.4, 'z': 20}, 2, 'hole')
        pin.set_pin({'x': 7, 'y': 23, 'z': 0.04}, 2, 'slot')
        pin.set_pin({'x': 13, 'y': -0.3, 'z': 0}, 3, 'slot')

        self.assertEqual(pin.get_pin(0, 'hole').tolist(), [1, 2, 0])
        self.assertEqual(pin.get_pin(0, 'slot').tolist(), [1, 0, 0.2])
        self.assertEqual(pin.get_pin(1, 'hole').tolist(), [5, 3, -10])
        self.assertEqual(pin.get_pin(1, 'slot').tolist(), [0, 1, 3])
        self.assertEqual(pin.get_pin(2, 'hole').tolist(), [-9, 0.4, 20])
        self.assertEqual(pin.get_pin(2, 'slot').tolist(), [7, 23, 0.04])
        self.assertEqual(pin.get_pin(3, 'hole').tolist(), [0, 0, 0])
        self.assertEqual(pin.get_pin(3, 'slot').tolist(), [13, -0.3, 0])

    def test_invalid_input(self):
        with self.assertWarns(UserWarning):
            pin = Pin()

        with self.assertRaises(ValueError):
            pin.set_pin(2, 3, 'hole')

        with self.assertRaises(ValueError):
            pin.set_pin([1, 2, 3], 2, 'hole')

        with self.assertRaises(ValueError):
            pin.set_pin({'x': 1, 'y': 2, 'z': 0}, 4, 'hole')

        with self.assertRaises(ValueError):
            pin.set_pin({'x': 1, 'y': 2, 'z': 0}, 3, 'foo')


if __name__ == '__main__':
    unittest.main()
