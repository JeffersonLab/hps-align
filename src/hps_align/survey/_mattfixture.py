
import numpy as np

from ._utils import *
from ._parser import Parser
from ._cli import app
from ._fixture import Fixture


class MattFixture(Fixture):
    """Fixture class for Matt's survey measurement

    The coordinate system was changed during the measurement.
    The ball positions are in OGP coordinates, the pin positions and base planes are in the new coordinate system ('Matt system').
    It appears like the new coordinate system is related to the fixture ball frame.

    Attributes
    ----------
    oriball_dict : dict
        Dictionary of ball coordinates {'x': x, 'y': y, 'z': z}, origin of ball frame
    diagball_dict : dict
        Dictionary of ball coordinates {'x': x, 'y': y, 'z': z}
    axiball_dict : dict
        Dictionary of ball coordinates {'x': x, 'y': y, 'z': z}
    ball_plane_dict : dict
        Dictionary of ball plane coordinates {'x': x, 'y': y, 'z': z, 'xy_angle': xy_angle, 'elevation': elevation}
    base_plane_dict : dict
        Dictionary of base plane coordinates {'x': x, 'y': y, 'z': z, 'xy_angle': xy_angle, 'elevation': elevation}
    oripin_dict : dict
        Dictionary of pin coordinates {'x': x, 'y': y, 'z': z}, slot side
    axipin_dict : dict
        Dictionary of pin coordinates {'x': x, 'y': y, 'z': z}, hole side
    """

    def __init__(self, input_file=None):
        self.parser = None
        super().__init__(input_file)

        if self.parser:
            self.oriball_dict = self.parser.get_coords('oriball')
            self.diagball_dict = self.parser.get_coords('diagball')
            self.axiball_dict = self.parser.get_coords('axiball')
            self.ball_plane_dict = self.parser.get_coords('Step:  5', 20)
            self.base_plane_dict = self.parser.get_coords('L0 base plane')
            self.oripin_dict = self.parser.get_coords('axipin')
            self.axipin_dict = self.parser.get_coords('oripin')

    def get_base_plane(self):
        """Get base plane coordinates. This is in Matt's coordinates.

        The coordinates are either read from survey data file or have been set manually before.

        Returns
        -------
        origin : np.array
            Base plane origin in Matt's coordinates
        normal : np.array
            Normal vector of base plane in Matt's coordinates
        """
        origin = np.array([self.base_plane_dict['x'], self.base_plane_dict['y'], self.base_plane_dict['z']])
        normal = normal_vector(self.base_plane_dict['xy_angle'], self.base_plane_dict['elevation'])
        return origin, normal

    def set_ball_plane(self, ball_plane_coords):
        """Set base plane coordinates

        Overwrites the base plane coordinates from the survey data file.

        Parameters
        ----------
        base_plane_coords : dict
            Dictionary of base plane coordinates
        """
        if not isinstance(ball_plane_coords, dict):
            raise ValueError('Invalid base plane coordinate type: {}'.format(ball_plane_coords))

        self.ball_plane_dict = ball_plane_coords

    def get_ball_plane(self):
        """Get base plane coordinates from survey data file

        Returns
        -------
        origin : np.array
            Base plane origin in Matt's coordinates
        normal : np.array
            Normal vector of base plane in Matt's coordinates
        """
        origin = np.array([self.ball_plane_dict['x'], self.ball_plane_dict['y'], self.ball_plane_dict['z']])
        normal = normal_vector(self.ball_plane_dict['xy_angle'], self.ball_plane_dict['elevation'])
        return origin, normal

    def get_pin(self, type):
        """Get pin coordinates from survey data file

        Parameters
        ----------
        type : str
            Type of pin to get coordinates for
        Returns
        -------
        pin : np.array
            Pin position in Matt's coordinates
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

        Returns
        -------
        basis : np.array
            Basis vectors in Matt's coordinates
        origin : np.array
            Origin in Matt's coordinates
        """
        slot_pin = self.get_pin('oripin')
        hole_pin = self.get_pin('axipin')

        plane_origin, plane_normal = self.get_base_plane()

        hole_pin_projected = project_to_plane(hole_pin, plane_origin, plane_normal)
        slot_pin_projected = project_to_plane(slot_pin, plane_origin, plane_normal)

        slot_to_hole = hole_pin_projected - slot_pin_projected
        basis = make_basis(slot_to_hole, plane_normal)
        origin = hole_pin_projected

        return basis, origin

    def get_matt_basis(self):
        """Get basis vectors for Matt sensor

        Returns
        -------
        basis : np.array
            Basis vectors in OGP (or other global) coordinates
        origin : np.array
            Origin in OGP (or other global) coordinates
        """
        origin = self.get_ball('oriball')
        vec1 = self.get_ball('axiball') - origin
        vec2 = self.get_ball_plane()[1]
        basis = make_basis(vec1, vec2)

        return np.array([basis[0], -basis[2], basis[1]]), origin

    def matt_to_ball(self):
        """Get transformation matrix from Matt coordinates to fixture ball frame

        This is just a rotation, no translation.

        Returns
        -------
        transformation : np.array
            Transformation matrix from Matt coordinates to fixture ball frame
        """
        ball_basis = self.get_ball_basis()[0]  # ball basis in OGP coordinates
        matt_basis = self.get_matt_basis()[0]  # Matt basis in OGP coordinates

        return np.matmul(matt_basis, np.linalg.inv(ball_basis))

    def get_pin_in_ball(self):
        """Get basis vectors for pin frame in fixture ball coordinates

        Returns
        -------
        basis : np.array
            Basis vectors in fixture ball coordinates
        origin : np.array
            Origin in fixture ball coordinates
        """
        basis, origin = self.get_pin_basis()
        basis = np.matmul(basis, self.matt_to_ball())
        origin = np.matmul(origin, self.matt_to_ball())
        return basis, origin
