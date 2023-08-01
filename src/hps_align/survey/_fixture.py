
import numpy as np

from ._utils import *
from ._parser import Parser
from ._cli import app


class Fixture:

    def __init__(self, input_file):
        self.input_file = input_file
        self.parser = Parser(input_file)

        self.oriball_dict = self._find_oriball()
        self.diagball_dict = self._find_diagball()
        self.axiball_dict = self._find_axiball()

    def _find_oriball(self):
        """Find oriball coordinates in survey data file

        Returns
        -------
        oriball : dict
            Dictionary of oriball coordinates
        """
        oriball = self.parser.find_coords(
            self.parser.find_names(['oriball'])['oriball'] + 1)
        return oriball

    def _find_diagball(self):
        """Find diagball coordinates in survey data file

        Returns
        -------
        diagball : dict
            Dictionary of diagball coordinates
        """
        diagball = self.parser.find_coords(
            self.parser.find_names(['diagball'])['diagball'] + 1)
        return diagball

    def _find_axiball(self):
        """Find axiball coordinates in survey data file

        Returns
        -------
        axiball : dict
            Dictionary of axiball coordinates
        """
        axiball = self.parser.find_coords(
            self.parser.find_names(['axiball'])['axiball'] + 1)
        return axiball

    def _find_base_plane(self):
        """Find base plane coordinates in survey data file

        Returns
        -------
        base_plane : dict
            Dictionary of base plane coordinates
        """
        base_plane = self.parser.find_coords(
            self.parser.find_names(['L0 base plane'])['L0 base plane'] + 1)
        return base_plane

    def _find_oripin(self):
        """Find oripin coordinates in survey data file

        Returns
        -------
        oripin : dict
            Dictionary of oripin coordinates
        """
        oripin = self.parser.find_coords(
            self.parser.find_names(['oripin'])['oripin'] + 1)
        return oripin

    def _find_axipin(self):
        """Find axipin coordinates in survey data file

        Returns
        -------
        axipin : dict
            Dictionary of axipin coordinates
        """
        axipin = self.parser.find_coords(
            self.parser.find_names(['axipin'])['axipin'] + 1)
        return axipin

    def set_ball(self, ball_coords, type):
        """Set ball coordinates for a given layer and ball type"""
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
        base_plane = self._find_base_plane()
        origin = np.array([base_plane['x'], base_plane['y'], base_plane['z']])
        normal = normal_vector(math.radians(base_plane['xy_angle']), math.radians(base_plane['elevation']))
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
            pin = self._find_oripin()
        elif type == 'axipin':
            pin = self._find_axipin()
        else:
            raise ValueError('Invalid pin type: {}'.format(type))
        return np.array([pin['x'], pin['y'], pin['z']])

    def get_pin_basis(self, volume):
        """Get basis vectors for pin frame

        This is in fixture ball coordinates if read from Matt's survey data file

        Parameters
        ----------
        volume : str
            "top" or "bottom"
        Returns
        -------
        basis : np.array
            Array of basis vectors
        origin : np.array
            Array of origin coordinates
        """
        if volume == 'top':
            slot_pin = self.get_pin('oripin')
            hole_pin = self.get_pin('axipin')
        elif volume == 'bottom':
            slot_pin = self.get_pin('axipin')
            hole_pin = self.get_pin('oripin')
        else:
            raise ValueError('Invalid volume: {}'.format(volume))

        plane_origin, plane_normal = self.get_base_plane()

        hole_pin_projected = project_to_plane(hole_pin, plane_origin, plane_normal)
        slot_pin_projected = project_to_plane(slot_pin, plane_origin, plane_normal)

        hole_to_slot = slot_pin_projected - hole_pin_projected
        basis = make_basis(hole_to_slot, plane_normal)
        origin = hole_pin_projected

        return basis, origin
