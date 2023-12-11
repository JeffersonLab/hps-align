
import numpy as np

from ._utils import *
from ._parser import Parser
from ._cli import app


class Fixture:
    """Fixture for measuring sensors

    The fixture is used to measure the sensors. It consists of a base plane, a ball frame and a pin frame.
    The pins are used to align the sensors and have the same distance as the uchannel pins.
    Additionally, the pin frame in the fixture is defined analogously to the uchannel pin frame.
    The pin positions cannot be used as a reference for meaurement once the sensor is installed.
    The fixture ball frame is used as a reference frame for the sensor measurements.
    Importantly, the fixture ball frame is not the same as the uchannel ball frame.
    Here, the ball frame is defined by three balls on the outside of the fixture.

    All measurements should be in the same global coordinate system, e.g. OGP.

    Attributes
    ----------
    oriball_dict : dict
        Dictionary of fixture ball coordinates {'x': x, 'y': y, 'z': z}, origin of ball frame
    diagball_dict : dict
        Dictionary of fixture ball coordinates {'x': x, 'y': y, 'z': z}
    axiball_dict : dict
        Dictionary of fixture ball coordinates {'x': x, 'y': y, 'z': z}
    ball_plane_dict : dict
        Dictionary of fixture ball coordinates {'x': x, 'y': y, 'z': z, 'xy_angle': xy_angle, 'elevation': elevation}
    base_plane_dict : dict
        Dictionary of base plane coordinates {'x': x, 'y': y, 'z': z, 'xy_angle': xy_angle, 'elevation': elevation}
    oripin_dict : dict
        Dictionary of pin coordinates {'x': x, 'y': y, 'z': z}, slot side
    axipin_dict : dict
        Dictionary of pin coordinates {'x': x, 'y': y, 'z': z}, hole side
    """
    def __init__(self, input_file=None):
        if input_file is None:
            self.oriball_dict = {'x': 0, 'y': 0, 'z': 0}
            self.diagball_dict = {'x': 0, 'y': 0, 'z': 0}
            self.axiball_dict = {'x': 0, 'y': 0, 'z': 0}
            self.ball_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0}
            self.base_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0}
            self.oripin_dict = {'x': 0, 'y': 0, 'z': 0}
            self.axipin_dict = {'x': 0, 'y': 0, 'z': 0}
            return

        self.parser = Parser(input_file)

    def set_ball(self, ball_coords, type):
        """Set fixture ball coordinates for a given layer and ball type

        Overwrites the fixture ball coordinates from the survey data file.

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
        """Get fixture ball coordinates from survey data file

        The coordinates are either read from survey data file or have been set manually before.

        Parameters
        ----------
        type : str
            Type of ball to get coordinates for
        Returns
        -------
        ball : np.array
            Ball position in OGP (or other global) coordinates
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
            Basis vectors in OGP (or other global) coordinates
        origin : np.array
            Origin in OGP (or other global) coordinates
        """
        origin = self.get_ball('oriball')
        basis = make_basis(self.get_ball('axiball') - origin, self.get_ball('diagball') - origin)

        return basis, origin

    def set_base_plane(self, base_plane_coords):
        """Set base plane coordinates

        Overwrites the base plane coordinates from the survey data file.

        Parameters
        ----------
        base_plane_coords : dict
            Dictionary of base plane coordinates
        """
        if not isinstance(base_plane_coords, dict):
            raise ValueError('Invalid base plane coordinate type: {}'.format(base_plane_coords))

        self.base_plane_dict = base_plane_coords

    def get_base_plane(self):
        """Get base plane coordinates.

        The coordinates are either read from survey data file or have been set manually before.

        Returns
        -------
        origin : np.array
            Base plane origin in OGP (or other global) coordinates
        normal : np.array
            Normal vector of base plane in OGP (or other global) coordinates
        """
        origin = np.array([self.base_plane_dict['x'], self.base_plane_dict['y'], self.base_plane_dict['z']])
        normal = normal_vector(self.base_plane_dict['xy_angle'], self.base_plane_dict['elevation'])
        return origin, normal

    def set_pin(self, pin_coords, type):
        """Set pin coordinates for a given layer and pin type

        Overwrites the pin coordinates from the survey data file.

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
        """Get pin coordinates.

        The coordinates are either read from survey data file or have been set manually before.

        Parameters
        ----------
        type : str
            Type of pin to get coordinates for
        Returns
        -------
        pin : np.array
            Pin position in OGP (or other global) coordinates
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
            Basis vectors in OGP (or other global) coordinates
        origin : np.array
            Origin in OGP (or other global) coordinates
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

    def get_pin_in_ball(self):
        """Get basis vectors for pin frame in fixture ball coordinates

        Returns
        -------
        basis : np.array
            Basis vectors in fixture ball frame
        origin : np.array
            Origin in fixture ball frame
        """
        pin_basis, pin_origin = self.get_pin_basis()
        ball_basis, ball_origin = self.get_ball_basis()

        basis = np.matmul(pin_basis, np.linalg.inv(ball_basis))
        origin = pin_origin - ball_origin
        origin = np.matmul(origin, np.linalg.inv(ball_basis))

        return basis, origin

    def get_ball_in_pin(self):
        basis, origin = self.get_pin_in_ball()
        return np.linalg.inv(basis), -np.matmul(origin, np.linalg.inv(basis))


class ShoFixture(Fixture):
    """Fixture class for Sho's survey measurement

    The coordinate system was changed during the measurement.
    The pin positions are in OGP coordinates, the ball positions are in the new coordinate system.
    It appears like the new coordinate system is related to the pin frame.
    """

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

    def get_sho_basis(self):
        """Get basis vectors for Sho's coordinate system

        Returns
        -------
        basis : np.array
            Basis vectors in OGP (or other global) coordinates
        origin : np.array
            Origin in OGP (or other global) coordinates
        """
        slot_pin = self.get_pin('oripin')
        hole_pin = self.get_pin('axipin')

        plane_origin, plane_normal = self.get_base_plane()

        hole_pin_projected = project_to_plane(hole_pin, plane_origin, plane_normal)
        slot_pin_projected = project_to_plane(slot_pin, plane_origin, plane_normal)

        hole_to_slot = slot_pin_projected - hole_pin_projected
        basis = make_basis(hole_to_slot, plane_normal)
        origin = hole_pin_projected

        return np.array([basis[0], -basis[2], basis[1]]), origin

    def sho_to_pin(self):
        """Get transformation matrix from Sho to fixture pin frame

        Returns
        -------
        transformation : np.array
            Transformation matrix from Sho to fixture pin frame
        """
        pin_basis = self.get_pin_basis()[0]  # this is in OGP coordinates
        sho_basis = self.get_sho_basis()[0]  # this is in OGP coordinates

        return np.matmul(sho_basis, np.linalg.inv(pin_basis))

    def get_ball_in_pin(self):
        """Get basis vectors for ball frame in fixture pin frame

        Returns
        -------
        basis : np.array
            Ball basis vectors in fixture pin frame
        origin : np.array
            Origin in fixture pin frame
        """
        ball_basis, ball_origin = self.get_ball_basis()  # this is in sho coordinates
        ball_basis = np.matmul(ball_basis, self.sho_to_pin())
        ball_origin = np.matmul(ball_origin, self.sho_to_pin())

        return ball_basis, ball_origin

    def get_pin_in_ball(self):
        """Get basis vectors for pin frame in fixture ball frame

        Returns
        -------
        basis : np.array
            Pin basis vectors in fixture ball frame
        origin : np.array
            Origin in fixture ball frame
        """
        ball_basis, ball_origin = self.get_ball_in_pin()
        return np.linalg.inv(ball_basis), -np.matmul(ball_origin, np.linalg.inv(ball_basis))
