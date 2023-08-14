
import numpy as np

import warnings

from ._utils import *
from ._parser import Parser
from ._cli import app


class Fixture:

    def __init__(self, input_file=None):
        if input_file is None:
            warnings.warn('No input file specified')
            self.oriball_dict = {'x': 0, 'y': 0, 'z': 0}
            self.diagball_dict = {'x': 0, 'y': 0, 'z': 0}
            self.axiball_dict = {'x': 0, 'y': 0, 'z': 0}
            self.ball_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0}
            self.base_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0}
            self.oripin_dict = {'x': 0, 'y': 0, 'z': 0}
            self.axipin_dict = {'x': 0, 'y': 0, 'z': 0}
            return

        self.input_file = input_file
        self.parser = Parser(input_file)

    def set_ball(self, ball_coords, type):
        """Set ball coordinates for a given layer and ball type

        Parameters
        ----------
        ball_coords : dict
            Dictionary of ball coordinates
        type : str
            Type of ball to set coordinates for
        """
        if not isinstance(ball_coords, dict):
            raise ValueError('Invalid ball coordinate type: {}'.format(ball_coords))

        if type == 'oriball':
            self.oriball_dict = ball_coords
        elif type == 'diagball':
            self.diagball_dict = ball_coords
        elif type == 'axiball':
            self.axiball_dict = ball_coords
        else:
            raise ValueError('Invalid ball type: {}'.format(type))

    def get_ball(self, type):
        """Get ball coordinates from survey data file

        Parameters
        ----------
        type : str
            Type of ball to get coordinates for
        Returns
        -------
        ball : np.array
            Array of ball coordinates
        """
        if type == 'oriball':
            ball = self.oriball_dict
        elif type == 'diagball':
            ball = self.diagball_dict
        elif type == 'axiball':
            ball = self.axiball_dict
        else:
            raise ValueError('Invalid ball type: {}'.format(type))
        return np.array([ball['x'], ball['y'], ball['z']])

    def get_ball_basis(self):
        """Get basis vectors for fixture

        Returns
        -------
        basis : np.array
            Array of basis vectors
        origin : np.array
            Array of origin coordinates
        """
        origin = self.get_ball('oriball')
        basis = make_basis(self.get_ball('axiball') - origin, self.get_ball('diagball') - origin)

        return basis, origin

    def set_base_plane(self, base_plane_coords):
        """Set base plane coordinates

        Parameters
        ----------
        base_plane_coords : dict
            Dictionary of base plane coordinates
        """
        if not isinstance(base_plane_coords, dict):
            raise ValueError('Invalid base plane coordinate type: {}'.format(base_plane_coords))

        self.base_plane_dict = base_plane_coords

    def get_base_plane(self):
        """Get base plane coordinates from survey data file

        This is in fixture ball coordinates if read from Matt's survey data file

        Returns
        -------
        origin : np.array
            Coordinates of base plane origin
        normal : np.array
            Normal vector of base plane
        """
        origin = np.array([self.base_plane_dict['x'], self.base_plane_dict['y'], self.base_plane_dict['z']])
        normal = normal_vector(self.base_plane_dict['xy_angle'], self.base_plane_dict['elevation'])
        return origin, normal

    def set_pin(self, pin_coords, type):
        """Set pin coordinates for a given layer and pin type

        Parameters
        ----------
        pin_coords : dict
            Dictionary of pin coordinates
        type : str
            Type of pin to set coordinates for
        """
        if not isinstance(pin_coords, dict):
            raise ValueError('Invalid pin coordinate type: {}'.format(pin_coords))

        if type == 'oripin':
            self.oripin_dict = pin_coords
        elif type == 'axipin':
            self.axipin_dict = pin_coords
        else:
            raise ValueError('Invalid pin type: {}'.format(type))

    def get_pin(self, type):
        """Get pin coordinates from survey data file

        This is in fixture ball coordinates if read from Matt's survey data file

        Parameters
        ----------
        type : str
            Type of pin to get coordinates for
        Returns
        -------
        pin : np.array
            Array of pin coordinates
        """
        if type == 'oripin':
            pin = self.oripin_dict
        elif type == 'axipin':
            pin = self.axipin_dict
        else:
            raise ValueError('Invalid pin type: {}'.format(type))
        return np.array([pin['x'], pin['y'], pin['z']])

    def get_pin_basis(self):
        """Get basis vectors for pin frame

        This is in fixture ball coordinates if read from Matt's survey data file

        Returns
        -------
        basis : np.array
            Array of basis vectors
        origin : np.array
            Array of origin coordinates
        """
        slot_pin = self.get_pin('oripin')
        hole_pin = self.get_pin('axipin')

        plane_origin, plane_normal = self.get_base_plane()

        hole_pin_projected = project_to_plane(hole_pin, plane_origin, plane_normal)
        slot_pin_projected = project_to_plane(slot_pin, plane_origin, plane_normal)

        hole_to_slot = slot_pin_projected - hole_pin_projected
        basis = make_basis(hole_to_slot, plane_normal)
        origin = hole_pin_projected

        return basis, origin

    def get_pin_in_ball(self):
        """Get basis vectors for pin frame in fixture ball coordinates

        Returns
        -------
        basis : np.array
            Array of basis vectors
        origin : np.array
            Array of origin coordinates
        """
        pin_basis, pin_origin = self.get_pin_basis()
        ball_basis, ball_origin = self.get_ball_basis()

        basis = np.matmul(pin_basis, np.linalg.inv(ball_basis))
        origin = pin_origin - ball_origin
        origin = np.matmul(origin, np.linalg.inv(ball_basis))

        return basis, origin


class ShoFixture(Fixture):

    def __init__(self, input_file=None):
        self.parser = None
        super().__init__(input_file)

        if self.parser:
            # ball coordinated in pin frame
            self.oriball_dict = self.parser.get_coords('Step 15 - Origin ball', 5)
            self.diagball_dict = self.parser.get_coords('Step 16 - Diagonal ball', 5)
            self.axiball_dict = self.parser.get_coords('Step 17 - Axis ball', 5)
            self.base_plane_dict = self.parser.get_coords('Step 9 - Datum plane', 7)
            # pin coordinates in OGP frame
            self.oripin_dict = self.parser.get_coords('Step 11 - Slot pin', 6)
            self.axipin_dict = self.parser.get_coords('Step 10 - Hole pin', 6)

    def get_ball_in_pin(self):
        return self.get_ball_basis()

    def get_pin_in_ball(self):
        ball_basis, ball_origin = self.get_ball_in_pin()
        return np.linalg.inv(ball_basis), -np.matmul(ball_origin, np.linalg.inv(ball_basis))


class MattFixture(Fixture):

    def __init__(self, input_file=None):
        self.parser = None
        super().__init__(input_file)

        if self.parser:
            self.oriball_dict = self.parser.get_coords('oriball')
            self.diagball_dict = self.parser.get_coords('diagball')
            self.axiball_dict = self.parser.get_coords('axiball')
            self.ball_plane_dict = self.parser.get_coords('Step:  5', 20)
            self.base_plane_dict = self.parser.get_coords('L0 base plane')
            self.oripin_dict = self.parser.get_coords('oripin')
            self.axipin_dict = self.parser.get_coords('axipin')

    def get_matt_basis(self):
        """Get basis vectors for Matt sensor

        Returns
        -------
        basis : np.array
            Array of basis vectors
        origin : np.array
            Array of origin coordinates
        """
        origin = self.get_ball('oriball')
        vec1 = self.get_ball('axiball') - origin
        vec2 = normal_vector(self.ball_plane_dict["xy_angle"], self.ball_plane_dict["elevation"])
        basis = make_basis(vec1, vec2)

        return np.array([basis[0], -basis[2], basis[1]]), origin

    def matt_to_ball(self):
        """Get transformation matrix from Matt to fixture ball frame
        
        This is just a rotation, no translation.
        """
        ball_basis = self.get_ball_basis()[0]
        matt_basis = self.get_matt_basis()[0]

        return np.matmul(matt_basis, np.linalg.inv(ball_basis))

    def get_pin_in_ball(self):
        """Get basis vectors for pin frame in fixture ball coordinates

        Returns
        -------
        basis : np.array
            Array of basis vectors
        origin : np.array
            Array of origin coordinates
        """
        basis, origin = self.get_pin_basis()
        basis = np.matmul(basis, self.matt_to_ball())
        origin = np.matmul(origin, self.matt_to_ball())
        return basis, origin

    def get_ball_in_pin(self):
        basis, origin = self.get_pin_in_ball()
        return np.linalg.inv(basis), -np.matmul(origin, np.linalg.inv(basis))
