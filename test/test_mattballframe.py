
import unittest

from hps_align.survey._ballframe import MattBallFrame


class TestInit(unittest.TestCase):

    def test_no_input(self):
        ballframe = MattBallFrame()

        empty_dict = {'x': 0, 'y': 0, 'z': 0}
        self.assertEqual(empty_dict, ballframe.L1_hole_ball_dict)
        self.assertEqual(empty_dict, ballframe.L1_slot_ball_dict)
        self.assertEqual(empty_dict, ballframe.L3_hole_ball_dict)
        self.assertEqual(empty_dict, ballframe.L3_slot_ball_dict)
        self.assertEqual(empty_dict, ballframe.L1_midpoint_dict)
        self.assertEqual(empty_dict, ballframe.L3_midpoint_dict)


class TestGetMidpoint(unittest.TestCase):

    def test_valid_input(self):
        ballframe = MattBallFrame()

        self.assertEqual(ballframe.get_midpoint(1).tolist(), [0.0, 0.0, 0.0])
        self.assertEqual(ballframe.get_midpoint(3).tolist(), [0.0, 0.0, 0.0])

    def test_invalid_input(self):
        ballframe = MattBallFrame()

        with self.assertRaises(ValueError):
            ballframe.get_meas_midpoint(2)


class TestSetMidpoint(unittest.TestCase):

    def test_valid_input(self):
        ballframe = MattBallFrame()

        ballframe.set_midpoint({'x': 1, 'y': 2, 'z': 0}, 1)
        ballframe.set_midpoint({'x': 5, 'y': 3, 'z': 0}, 3)

        self.assertEqual(ballframe.get_meas_midpoint(1).tolist(), [1, 2, 0])
        self.assertEqual(ballframe.get_meas_midpoint(3).tolist(), [5, 3, 0])

    def test_invalid_input(self):
        ballframe = MattBallFrame()

        with self.assertRaises(ValueError):
            ballframe.set_midpoint(1, 1)

        with self.assertRaises(ValueError):
            ballframe.set_midpoint([1, 2, 3], 1)

        with self.assertRaises(ValueError):
            ballframe.set_midpoint({'x': 0, 'y': 0, 'z': 0}, 2)


class TestGetBasis(unittest.TestCase):

    def test_get_matt_basis(self):
        ballframe = MattBallFrame()

        # top
        ballframe.set_ball({'x': 2, 'y': 1, 'z': 0}, 1, 'hole')
        ballframe.set_ball({'x': 0, 'y': 1, 'z': 0}, 1, 'slot')
        ballframe.set_midpoint({'x': 1, 'y': 1, 'z': 0}, 1)
        ballframe.set_ball({'x': 2, 'y': 5, 'z': 0}, 3, 'hole')
        ballframe.set_ball({'x': 0, 'y': 5, 'z': 0}, 3, 'slot')
        ballframe.set_midpoint({'x': 1, 'y': 5, 'z': 0}, 3)

        basis, origin = ballframe.get_matt_basis('top')
        self.assertEqual(origin.tolist(), [1, 1, 0])
        self.assertEqual(basis[0].tolist(), [0, 1, 0])
        self.assertEqual(basis[1].tolist(), [1, 0, 0])
        self.assertEqual(basis[2].tolist(), [0, 0, -1])

        # bottom
        ballframe.set_ball({'x': 2, 'y': 1, 'z': 0}, 1, 'slot')
        ballframe.set_ball({'x': 0, 'y': 1, 'z': 0}, 1, 'hole')
        ballframe.set_midpoint({'x': 1, 'y': 1, 'z': 0}, 1)
        ballframe.set_ball({'x': 2, 'y': 5, 'z': 0}, 3, 'slot')
        ballframe.set_ball({'x': 0, 'y': 5, 'z': 0}, 3, 'hole')
        ballframe.set_midpoint({'x': 1, 'y': 5, 'z': 0}, 3)

        basis, origin = ballframe.get_matt_basis('bottom')
        self.assertEqual(origin.tolist(), [1, 1, 0])
        self.assertEqual(basis[0].tolist(), [0, 1, 0])
        self.assertEqual(basis[1].tolist(), [1, 0, 0])
        self.assertEqual(basis[2].tolist(), [0, 0, -1])

    def test_get_basis(self):
        ballframe = MattBallFrame()

        # top
        ballframe.set_ball({'x': 2, 'y': 1, 'z': 0}, 1, 'hole')
        ballframe.set_ball({'x': 0, 'y': 1, 'z': 0}, 1, 'slot')
        ballframe.set_midpoint({'x': 1, 'y': 1, 'z': 0}, 1)
        ballframe.set_ball({'x': 2, 'y': 5, 'z': 0}, 3, 'hole')
        ballframe.set_ball({'x': 0, 'y': 5, 'z': 0}, 3, 'slot')
        ballframe.set_midpoint({'x': 1, 'y': 5, 'z': 0}, 3)

        basis, origin = ballframe.get_basis('top')
        self.assertEqual(origin.tolist(), [0, 0, 0])
        self.assertEqual(basis[0].tolist(), [0, -1, 0])
        self.assertEqual(basis[1].tolist(), [0, 0, -1])
        self.assertEqual(basis[2].tolist(), [1, 0, 0])

        # bottom
        ballframe.set_ball({'x': 2, 'y': 1, 'z': 0}, 1, 'slot')
        ballframe.set_ball({'x': 0, 'y': 1, 'z': 0}, 1, 'hole')
        ballframe.set_midpoint({'x': 1, 'y': 1, 'z': 0}, 1)
        ballframe.set_ball({'x': 2, 'y': 5, 'z': 0}, 3, 'slot')
        ballframe.set_ball({'x': 0, 'y': 5, 'z': 0}, 3, 'hole')
        ballframe.set_midpoint({'x': 1, 'y': 5, 'z': 0}, 3)

        basis, origin = ballframe.get_basis('bottom')
        self.assertEqual(origin.tolist(), [0, 0, 0])
        self.assertEqual(basis[0].tolist(), [0, 1, 0])
        self.assertEqual(basis[1].tolist(), [0, 0, 1])
        self.assertEqual(basis[2].tolist(), [1, 0, 0])


if __name__ == '__main__':
    unittest.main()
