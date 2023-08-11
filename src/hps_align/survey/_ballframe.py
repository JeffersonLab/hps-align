
import warnings
from ._utils import *
from ._parser import Parser
from ._cli import app


class BallFrame:

    def __init__(self, input_file=None):
        """Initialize BallFrame object

        Parameters
        ----------
        input_file : str
            Survey data file
        """
        if input_file is None:
            warnings.warn('No input file specified')
            self.L1_hole_ball_dict = {'x': 0, 'y': 0, 'z': 0}
            self.L1_slot_ball_dict = {'x': 0, 'y': 0, 'z': 0}
            self.L3_hole_ball_dict = {'x': 0, 'y': 0, 'z': 0}
            self.L3_slot_ball_dict = {'x': 0, 'y': 0, 'z': 0}
            return

        # self.input_file = input_file
        self.parser = Parser(input_file)

    def set_ball(self, ball_coords, layer, ball_type):
        """Set ball coordinates for a given layer and ball type"""
        if not isinstance(ball_coords, dict):
            raise ValueError('Invalid ball coordinate type: {}'.format(ball_coords))

        if layer == 1:
            if ball_type == 'hole':
                self.L1_hole_ball_dict = ball_coords
            elif ball_type == 'slot':
                self.L1_slot_ball_dict = ball_coords
            else:
                raise ValueError('Invalid ball type: {}'.format(ball_type))
        elif layer == 3:
            if ball_type == 'hole':
                self.L3_hole_ball_dict = ball_coords
            elif ball_type == 'slot':
                self.L3_slot_ball_dict = ball_coords
            else:
                raise ValueError('Invalid ball type: {}'.format(ball_type))
        else:
            raise ValueError('Invalid layer: {}'.format(layer))

    def get_ball(self, layer, ball_type):
        """Get ball coordinates for a given layer and ball type

        Parameters
        ----------
        layer : int
            Layer number
        ball_type : str
            Ball type ('hole' or 'slot')

        Returns
        -------
        ball : np.array
            Numpy array of ball coordinates
        """
        if layer == 1:
            if ball_type == 'hole':
                ball = self.L1_hole_ball_dict
            elif ball_type == 'slot':
                ball = self.L1_slot_ball_dict
            else:
                raise ValueError('Invalid ball type: {}'.format(ball_type))
        elif layer == 3:
            if ball_type == 'hole':
                ball = self.L3_hole_ball_dict
            elif ball_type == 'slot':
                ball = self.L3_slot_ball_dict
            else:
                raise ValueError('Invalid ball type: {}'.format(ball_type))
        else:
            raise ValueError('Invalid layer: {}'.format(layer))

        return np.array([ball['x'], ball['y'], ball['z']])

    def get_basis(self, volume=''):
        """Get ballframe basis vectors

        Returns
        -------
        basis : np.array
            Numpy array of basis vectors
        origin : np.array
            Numpy array of origin coordinates
        """
        origin = self.get_ball(1, 'slot')

        vec1 = self.get_ball(1, 'hole')
        vec2 = self.get_ball(3, 'hole')
        hole_avg = (vec1 + vec2) / 2
        vec0 = self.get_ball(3, 'slot')
        basis = make_basis(vec0 - origin, hole_avg - origin)

        return np.array([-basis[1], -basis[2], basis[0]]), origin


class MattBallFrame(BallFrame):

    def __init__(self, input_file=None):
        self.parser = None
        super().__init__(input_file)

        if self.parser:
            self.L1_hole_ball_dict = self.parser.get_coords('L1 hole ball')
            self.L1_slot_ball_dict = self.parser.get_coords('L1 slot ball')
            self.L3_hole_ball_dict = self.parser.get_coords('L3 hole ball')
            self.L3_slot_ball_dict = self.parser.get_coords('L3 slot ball')

    def _find_L1_midpoint(self):
        """Find L1 midpoint (slot and hole) coordinates in survey data file

        Returns
        -------
        midpoint : dict
            Dictionary of L1 midpoint coordinates
        """
        midpoint = self.parser.find_coords(
            self.parser.find_names(['Step:  5'])['Step:  5'] + 1, 20)
        return midpoint

    def _find_L3_midpoint(self):
        """Find L3 midpoint (slot and hole) coordinates in survey data file

        Returns
        -------
        midpoint : dict
            Dictionary of L3 midpoint coordinates
        """
        midpoint = self.parser.find_coords(
            self.parser.find_names(['Step:  6'])['Step:  6'] + 1, 20)
        return midpoint

    def get_matt_basis(self, volume):
        """Get basis vectors for Matt's ballframe

        Parameters
        ----------
        volume : str
            'top' or 'bottom'

        Returns
        -------
        basis : np.array
            Numpy array of basis vectors
        origin : np.array
            Numpy array of origin coordinates
        """
        origin = self._find_L1_midpoint()
        origin = np.array([origin['x'], origin['y'], origin['z']])
        L3_midpoint = self._find_L3_midpoint()
        L3_midpoint = np.array([L3_midpoint['x'], L3_midpoint['y'], L3_midpoint['z']])

        if (volume == 'top'):
            basis = make_basis(L3_midpoint - origin, self.get_ball(1, 'hole') - origin)
        elif (volume == 'bottom'):
            basis = make_basis(L3_midpoint - origin, self.get_ball(1, 'slot') - origin)

        return basis, origin

    def get_basis(self, volume):
        """Get ballframe basis vectors

        Parameters
        ----------
        volume : str
            'top' or 'bottom'

        Returns
        -------
        basis : np.array
            Numpy array of basis vectors
        origin : np.array
            Numpy array of origin coordinates
        """
        basis_matt, origin_matt = self.get_matt_basis(volume)

        origin = self.get_ball(1, 'slot') - origin_matt
        origin = np.matmul(origin, np.linalg.inv(basis_matt))
        vec1 = np.matmul(self.get_ball(1, 'hole') - origin_matt, np.linalg.inv(basis_matt))
        vec2 = np.matmul(self.get_ball(3, 'hole') - origin_matt, np.linalg.inv(basis_matt))
        hole_avg = (vec1 + vec2) / 2
        vec0 = np.matmul(self.get_ball(3, 'slot') - origin_matt, np.linalg.inv(basis_matt))
        basis = make_basis(vec0 - origin, hole_avg - origin)

        return np.array([-basis[1], -basis[2], basis[0]]), origin
