
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

    def get_midpoint(self, layer):
        """Get midpoint between hole and slot balls for a given layer

        Parameters
        ----------
        layer : int
            Layer number

        Returns
        -------
        midpoint : np.array
            Numpy array of midpoint coordinates
        """
        hole_ball = self.get_ball(layer, 'hole')
        slot_ball = self.get_ball(layer, 'slot')
        midpoint = (hole_ball + slot_ball) / 2

        return midpoint

    def get_basis(self, volume=''):
        """Get ballframe basis vectors

        Returns
        -------
        basis : np.array
            Numpy array of basis vectors
        origin : np.array
            Numpy array of origin coordinates
        """

        origin = self.get_midpoint(1)

        vec1 = self.get_midpoint(3) - origin
        hole_to_slot1 = self.get_ball(1, 'slot') - self.get_ball(1, 'hole')
        hole_to_slot3 = self.get_ball(3, 'slot') - self.get_ball(3, 'hole')
        vec2 = (hole_to_slot1 + hole_to_slot3) / 2

        basis = make_basis(vec1, vec2)

        return np.array([basis[1], basis[2], basis[0]]), origin


class MattBallFrame(BallFrame):

    def __init__(self, input_file=None):
        self.parser = None
        self.L1_midpoint_dict = {'x': 0, 'y': 0, 'z': 0}
        self.L3_midpoint_dict = {'x': 0, 'y': 0, 'z': 0}
        super().__init__(input_file)

        if self.parser:
            self.L1_hole_ball_dict = self.parser.get_coords('L1 hole ball')
            self.L1_slot_ball_dict = self.parser.get_coords('L1 slot ball')
            self.L3_hole_ball_dict = self.parser.get_coords('L3 hole ball')
            self.L3_slot_ball_dict = self.parser.get_coords('L3 slot ball')
            self.L1_midpoint_dict = self.parser.get_coords('Step:  5', 20)
            self.L3_midpoint_dict = self.parser.get_coords('Step:  6', 20)

    def set_midpoint(self, midpoint_coords, layer):
        """Set midpoint coordinates for a given layer"""
        if not isinstance(midpoint_coords, dict):
            raise ValueError('Invalid midpoint coordinate type: {}'.format(midpoint_coords))

        if layer == 1:
            self.L1_midpoint_dict = midpoint_coords
        elif layer == 3:
            self.L3_midpoint_dict = midpoint_coords
        else:
            raise ValueError('Invalid layer: {}'.format(layer))

    def get_meas_midpoint(self, layer):
        """Get midpoint coordinates for a given layer

        Parameters
        ----------
        layer : int
            Layer number

        Returns
        -------
        midpoint : np.array
            Numpy array of midpoint coordinates
        """
        if layer == 1:
            midpoint = self.L1_midpoint_dict
        elif layer == 3:
            midpoint = self.L3_midpoint_dict
        else:
            raise ValueError('Invalid layer: {}'.format(layer))

        return np.array([midpoint['x'], midpoint['y'], midpoint['z']])

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
        origin = self.get_meas_midpoint(1)
        L3_midpoint = self.get_meas_midpoint(3)

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
        ball_basis, ball_origin = super().get_basis(volume)

        origin = np.matmul(ball_origin - origin_matt, np.linalg.inv(basis_matt))
        basis = np.matmul(ball_basis, np.linalg.inv(basis_matt))

        return basis, origin
