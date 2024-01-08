
import unittest
import numpy as np

from hps_align.survey._baseplanes import BasePlane


class TestInit(unittest.TestCase):

    def test_no_input(self):
        baseplanes = BasePlane()

        empty_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0}
        self.assertEqual(empty_dict, baseplanes.L0_base_plane_dict)
        self.assertEqual(empty_dict, baseplanes.L1_base_plane_dict)
        self.assertEqual(empty_dict, baseplanes.L2_base_plane_dict)
        self.assertEqual(empty_dict, baseplanes.L3_base_plane_dict)


class TestSetBasePlaneDict(unittest.TestCase):

    def test_valid_input(self):
        baseplanes = BasePlane()

        baseplanes.set_base_plane_dict({'x': 1, 'y': 2, 'z': 0, 'xy_angle': -0.8, 'elevation': 1.3}, 0)
        baseplanes.set_base_plane_dict({'x': 1, 'y': 0, 'z': 0.2, 'xy_angle': 0, 'elevation': 1}, 1)
        baseplanes.set_base_plane_dict({'x': 5, 'y': 3, 'z': -10, 'xy_angle': 3, 'elevation': 0.5}, 2)
        baseplanes.set_base_plane_dict({'x': -0.3, 'y': 1, 'z': 3, 'xy_angle': 0, 'elevation': -6}, 3)

        self.assertEqual(baseplanes.L0_base_plane_dict, {'x': 1, 'y': 2, 'z': 0, 'xy_angle': -0.8, 'elevation': 1.3})
        self.assertEqual(baseplanes.L1_base_plane_dict, {'x': 1, 'y': 0, 'z': 0.2, 'xy_angle': 0, 'elevation': 1})
        self.assertEqual(baseplanes.L2_base_plane_dict, {'x': 5, 'y': 3, 'z': -10, 'xy_angle': 3, 'elevation': 0.5})
        self.assertEqual(baseplanes.L3_base_plane_dict, {'x': -0.3, 'y': 1, 'z': 3, 'xy_angle': 0, 'elevation': -6})

    def test_invalid_input(self):
        baseplanes = BasePlane()

        with self.assertRaises(ValueError):
            baseplanes.set_base_plane_dict({'x': 1, 'y': 2, 'z': 0, 'xy_angle': -0.8, 'elevation': 1.3}, 4)


class TestGetBasePlane(unittest.TestCase):

    def test_origin(self):
        baseplanes = BasePlane()

        empty_list = [0, 0, 0]
        self.assertEqual(empty_list, baseplanes.get_base_plane(0)[0].tolist())
        self.assertEqual(empty_list, baseplanes.get_base_plane(1)[0].tolist())
        self.assertEqual(empty_list, baseplanes.get_base_plane(2)[0].tolist())
        self.assertEqual(empty_list, baseplanes.get_base_plane(3)[0].tolist())

        baseplanes.set_base_plane_dict({'x': 1, 'y': 2, 'z': 0, 'xy_angle': -0.8, 'elevation': 1.3}, 0)
        baseplanes.set_base_plane_dict({'x': 1, 'y': 0, 'z': 0.2, 'xy_angle': 0, 'elevation': 1}, 1)
        baseplanes.set_base_plane_dict({'x': 5, 'y': 3, 'z': -10, 'xy_angle': 3, 'elevation': 0.5}, 2)
        baseplanes.set_base_plane_dict({'x': -0.3, 'y': 1, 'z': 3, 'xy_angle': 0, 'elevation': -6}, 3)

        self.assertEqual([1, 2, 0], baseplanes.get_base_plane(0)[0].tolist())
        self.assertEqual([1, 0, 0.2], baseplanes.get_base_plane(1)[0].tolist())
        self.assertEqual([5, 3, -10], baseplanes.get_base_plane(2)[0].tolist())
        self.assertEqual([-0.3, 1, 3], baseplanes.get_base_plane(3)[0].tolist())

    def test_normal(self):
        baseplanes = BasePlane()

        self.assertEqual([1, 0, 0], baseplanes.get_base_plane(0)[1].tolist())
        self.assertEqual([1, 0, 0], baseplanes.get_base_plane(1)[1].tolist())
        self.assertEqual([1, 0, 0], baseplanes.get_base_plane(2)[1].tolist())
        self.assertEqual([1, 0, 0], baseplanes.get_base_plane(3)[1].tolist())

        baseplanes.set_base_plane_dict({'x': 1, 'y': 2, 'z': 0, 'xy_angle': np.pi/2, 'elevation': 0}, 0)
        self.assertAlmostEqual(0, baseplanes.get_base_plane(0)[1].tolist()[0])
        self.assertAlmostEqual(1, baseplanes.get_base_plane(0)[1].tolist()[1])
        self.assertAlmostEqual(0, baseplanes.get_base_plane(0)[1].tolist()[2])

        baseplanes.set_base_plane_dict({'x': 1, 'y': 0, 'z': 0.2, 'xy_angle': 0, 'elevation': np.pi/2}, 1)
        self.assertAlmostEqual(0, baseplanes.get_base_plane(1)[1].tolist()[0])
        self.assertAlmostEqual(0, baseplanes.get_base_plane(1)[1].tolist()[1])
        self.assertAlmostEqual(1, baseplanes.get_base_plane(1)[1].tolist()[2])

        baseplanes.set_base_plane_dict({'x': 5, 'y': 3, 'z': -10, 'xy_angle': np.pi/2, 'elevation': np.pi/4}, 2)
        self.assertAlmostEqual(0, baseplanes.get_base_plane(2)[1].tolist()[0])
        self.assertAlmostEqual(1/np.sqrt(2), baseplanes.get_base_plane(2)[1].tolist()[1])
        self.assertAlmostEqual(1/np.sqrt(2), baseplanes.get_base_plane(2)[1].tolist()[2])

        baseplanes.set_base_plane_dict({'x': -0.3, 'y': 1, 'z': 3, 'xy_angle': np.pi/2, 'elevation': -np.pi/4}, 3)
        self.assertAlmostEqual(0, baseplanes.get_base_plane(3)[1].tolist()[0])
        self.assertAlmostEqual(-1/np.sqrt(2), baseplanes.get_base_plane(3)[1].tolist()[1])
        self.assertAlmostEqual(1/np.sqrt(2), baseplanes.get_base_plane(3)[1].tolist()[2])

    def test_invalid_input(self):
        baseplanes = BasePlane()

        with self.assertRaises(ValueError):
            baseplanes.get_base_plane(4)


if __name__ == '__main__':
    unittest.main()
