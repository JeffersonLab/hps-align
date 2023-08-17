
import unittest

from hps_align.survey._ballframe import BallFrame


class TestInit(unittest.TestCase):

    def test_no_input(self):
        with self.assertWarns(UserWarning):
            ballframe = BallFrame()

        empty_dict = {'x': 0, 'y': 0, 'z': 0}
        self.assertEqual(empty_dict, ballframe.L1_hole_ball_dict)
        self.assertEqual(empty_dict, ballframe.L1_slot_ball_dict)
        self.assertEqual(empty_dict, ballframe.L3_hole_ball_dict)
        self.assertEqual(empty_dict, ballframe.L3_slot_ball_dict)


class TestGetBall(unittest.TestCase):

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            ballframe = BallFrame()

        self.assertEqual(ballframe.get_ball(1, 'hole').tolist(), [0.0, 0.0, 0.0])
        self.assertEqual(ballframe.get_ball(1, 'slot').tolist(), [0.0, 0.0, 0.0])
        self.assertEqual(ballframe.get_ball(3, 'hole').tolist(), [0.0, 0.0, 0.0])
        self.assertEqual(ballframe.get_ball(3, 'slot').tolist(), [0.0, 0.0, 0.0])

    def test_invalid_input(self):
        with self.assertWarns(UserWarning):
            ballframe = BallFrame()

        with self.assertRaises(ValueError):
            ballframe.get_ball(2, 'hole')

        with self.assertRaises(ValueError):
            ballframe.get_ball(1, 'foo')


class TestSetBall(unittest.TestCase):

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            ballframe = BallFrame()

        ballframe.set_ball({'x': 1, 'y': 2, 'z': 0}, 1, 'hole')
        ballframe.set_ball({'x': 1, 'y': 0, 'z': 0}, 1, 'slot')
        ballframe.set_ball({'x': 5, 'y': 3, 'z': 0}, 3, 'hole')
        ballframe.set_ball({'x': 5, 'y': 1, 'z': 0}, 3, 'slot')

        self.assertEqual(ballframe.get_ball(1, 'hole').tolist(), [1, 2, 0])
        self.assertEqual(ballframe.get_ball(1, 'slot').tolist(), [1, 0, 0])
        self.assertEqual(ballframe.get_ball(3, 'hole').tolist(), [5, 3, 0])
        self.assertEqual(ballframe.get_ball(3, 'slot').tolist(), [5, 1, 0])

    def test_invalid_input(self):
        with self.assertWarns(UserWarning):
            ballframe = BallFrame()

        with self.assertRaises(ValueError):
            ballframe.set_ball(1, 1, 'hole')

        with self.assertRaises(ValueError):
            ballframe.set_ball([1, 2, 3], 1, 'hole')

        with self.assertRaises(ValueError):
            ballframe.set_ball({'x': 0, 'y': 0, 'z': 0}, 2, 'hole')

        with self.assertRaises(ValueError):
            ballframe.set_ball({'x': 0, 'y': 0, 'z': 0}, 1, 'foo')


class TestGetMidpoint(unittest.TestCase):

    def test_valid_input(self):
        with self.assertWarns(UserWarning):
            ballframe = BallFrame()

        ballframe.set_ball({'x': 1, 'y': 2, 'z': 0}, 1, 'hole')
        ballframe.set_ball({'x': 1, 'y': 0, 'z': 0}, 1, 'slot')
        ballframe.set_ball({'x': 5, 'y': 3, 'z': 0}, 3, 'hole')
        ballframe.set_ball({'x': 5, 'y': 1, 'z': 0}, 3, 'slot')

        self.assertEqual(ballframe.get_midpoint(1).tolist(), [1, 1, 0])
        self.assertEqual(ballframe.get_midpoint(3).tolist(), [5, 2, 0])

    def test_invalid_input(self):
        with self.assertWarns(UserWarning):
            ballframe = BallFrame()

        with self.assertRaises(ValueError):
            ballframe.get_midpoint(2)


class TestGetBasis(unittest.TestCase):

    def test_get_basis(self):
        with self.assertWarns(UserWarning):
            ballframe = BallFrame()

        # top
        ballframe.set_ball({'x': 1, 'y': 2, 'z': 0}, 1, 'hole')
        ballframe.set_ball({'x': 1, 'y': 0, 'z': 0}, 1, 'slot')  # origin
        ballframe.set_ball({'x': 5, 'y': 2, 'z': 0}, 3, 'hole')
        ballframe.set_ball({'x': 5, 'y': 0, 'z': 0}, 3, 'slot')

        basis, origin = ballframe.get_basis()
        self.assertEqual(origin.tolist(), [1, 1, 0])
        self.assertEqual(basis[0].tolist(), [0, -1, 0])
        self.assertEqual(basis[1].tolist(), [0, 0, -1])
        self.assertEqual(basis[2].tolist(), [1, 0, 0])

        # bottom
        ballframe.set_ball({'x': 1, 'y': 0, 'z': 0}, 1, 'hole')
        ballframe.set_ball({'x': 1, 'y': 2, 'z': 0}, 1, 'slot')  # origin
        ballframe.set_ball({'x': 5, 'y': 0, 'z': 0}, 3, 'hole')
        ballframe.set_ball({'x': 5, 'y': 2, 'z': 0}, 3, 'slot')

        basis, origin = ballframe.get_basis()
        self.assertEqual(origin.tolist(), [1, 1, 0])
        self.assertEqual(basis[0].tolist(), [0, 1, 0])
        self.assertEqual(basis[1].tolist(), [0, 0, 1])
        self.assertEqual(basis[2].tolist(), [1, 0, 0])


if __name__ == '__main__':
    unittest.main()
