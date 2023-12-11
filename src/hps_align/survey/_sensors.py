
import numpy as np

from ._parser import Parser
from ._fixture import *
from ._utils import *
from ._cli import app


class Sensor:
    """SVT sensor class
    
    The sensors are measured while mounted in the fixture.
    In addition to the sensor's position and orientation, the position of the ficxture balls has to be measured.
    The sensor coordinates in the survey data file should be given in the OGP (or other global) system.

    Attributes
    ----------
    fixture : Fixture
        Fixture object
    oriball_dict : dict
        Dictionary of ball coordinates {'x': x, 'y': y, 'z': z}, origin of ball frame
    diagball_dict : dict
        Dictionary of ball coordinates {'x': x, 'y': y, 'z': z}
    axiball_dict : dict
        Dictionary of ball coordinates {'x': x, 'y': y, 'z': z}
    ball_plane_dict : dict
        Dictionary of ball plane coordinates {'x': x, 'y': y, 'z': z, 'xy_angle': xy_angle, 'elevation': elevation}
    sensor_plane_dict : dict
        Dictionary of sensor plane coordinates {'x': x, 'y': y, 'z': z, 'xy_angle': xy_angle, 'elevation': elevation}
    sensor_origin_dict : dict
        Dictionary of sensor origin coordinates {'x': x, 'y': y, 'z': z}
    """
    def __init__(self, fixture, input_file=None):

        self.fixture = fixture
        if input_file is None:
            self.oriball_dict = {'x': 0, 'y': 0, 'z': 0}
            self.diagball_dict = {'x': 0, 'y': 0, 'z': 0}
            self.axiball_dict = {'x': 0, 'y': 0, 'z': 0}
            self.ball_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0}
            self.sensor_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0}
            self.sensor_origin_dict = {'x': 0, 'y': 0, 'z': 0}
            return

        self.parser = Parser(input_file)

    def set_ball(self, ball_coords, balltype):
        """Set ball coordinates for a given layer and ball type

        Overwrites the ball coordinates from the survey data file.

        Parameters
        ----------
        ball_coords : dict
            Dictionary of ball coordinates
        type : str
            Type of ball to set coordinates for
        """
        if not isinstance(ball_coords, dict):
            raise ValueError('Invalid ball coordinate type: {}'.format(ball_coords))

        if balltype == 'oriball':
            self.oriball_dict = ball_coords
        elif balltype == 'diagball':
            self.diagball_dict = ball_coords
        elif balltype == 'axiball':
            self.axiball_dict = ball_coords
        else:
            raise ValueError('Invalid ball type: {}'.format(balltype))

    def get_ball(self, balltype):
        """Get ball coordinates from survey data file

        Parameters
        ----------
        balltype : str
            Type of ball to get coordinates for
        Returns
        -------
        ball : np.array
            Fixture ball position in OGP (or other global) coordinates
        """
        if balltype == 'oriball':
            ball = self.oriball_dict
        elif balltype == 'diagball':
            ball = self.diagball_dict
        elif balltype == 'axiball':
            ball = self.axiball_dict
        else:
            raise ValueError('Invalid ball type: {}'.format(balltype))
        return np.array([ball['x'], ball['y'], ball['z']])

    def get_ball_basis(self):
        """Get ball basis

        Returns
        -------
        basis : np.array
            Fixture ball basis vectors in OGP (or other global) coordinates
        origin : np.array
            Origin in OGP (or other global) coordinates
        """
        origin = self.get_ball('oriball')
        basis = make_basis(self.get_ball('axiball') - origin, self.get_ball('diagball') - origin)

        return basis, origin

    def set_sensor_origin(self, sensor_origin):
        """Set sensor origin coordinates

        Overwrites the sensor origin coordinates from the survey data file.

        Parameters
        ----------
        sensor_origin : dict
            Dictionary of sensor origin coordinates
        """
        if not isinstance(sensor_origin, dict):
            raise ValueError('Invalid sensor origin type: {}'.format(sensor_origin))

        self.sensor_origin_dict = sensor_origin

    def get_sensor_origin(self):
        """Get sensor origin coordinates

        Returns
        -------
        origin : np.array
            Sensor origin in OGP (or other global) coordinates
        """
        return np.array([self.sensor_origin_dict['x'], self.sensor_origin_dict['y'], self.sensor_origin_dict['z']])

    def get_sensor_origin_ballframe(self):
        """Get sensor origin coordinates in fixture ballframe

        Returns
        -------
        origin : np.array
            Sensor origin coordinates in fixture ballframe
        """
        ball_basis, ball_origin = self.get_ball_basis()  # in OGP coords
        origin = self.get_sensor_origin() - ball_origin  # in OGP coords
        origin = np.matmul(origin, np.linalg.inv(ball_basis))

        return origin

    def get_sensor_origin_pinframe(self):
        """Get sensor origin coordinates in pinframe

        Returns
        -------
        origin : np.array
            Sensor origin in fixture pinframe
        """
        origin = self.get_sensor_origin_ballframe()  # in fixture ballframe
        pin_in_ball_origin = self.fixture.get_pin_in_ball()[1]  # in fixture ballframe
        ball_in_pin_basis = self.fixture.get_ball_in_pin()[0]  # ball to pin
        origin = origin - pin_in_ball_origin  # in fixture ballframe
        origin = np.matmul(origin, ball_in_pin_basis)  # in pinframe

        return origin

    def set_sensor_plane(self, sensor_plane):
        """Set sensor plane coordinates

        Overwrites the sensor plane coordinates from the survey data file.

        Parameters
        ----------
        sensor_plane : dict
            Dictionary of sensor plane coordinates
        """
        if not isinstance(sensor_plane, dict):
            raise ValueError('Invalid sensor plane type: {}'.format(sensor_plane))

        self.sensor_plane_dict = sensor_plane

    def get_sensor_normal(self):
        """Get sensor normal vector

        Returns
        -------
        normal : np.array
            Normal vector to sensor plane in OGP (or other global) coordinates
        """
        return normal_vector(self.sensor_plane_dict["xy_angle"], self.sensor_plane_dict["elevation"])

    def get_sensor_normal_ballframe(self):
        """Get sensor normal coordinates in fixture ballframe

        Returns
        -------
        normal : np.array
            Sensor normal vector in fixture ballframe
        """
        ball_basis = self.get_ball_basis()[0]  # ball to OGP, inverse: OGP to ball
        normal = self.get_sensor_normal()  # in OGP coords
        normal = np.matmul(normal, np.linalg.inv(ball_basis))  # in ballframe

        return normal

    def get_sensor_normal_pinframe(self):
        """Get sensor normal vector in pinframe

        Returns
        -------
        normal : np.array
            Sensor normal vector in fixture pinframe
        """
        normal = self.get_sensor_normal_ballframe()  # in fixture ballframe
        ball_in_pin_basis = self.fixture.get_ball_in_pin()[0]  # ball to pin

        normal = np.matmul(normal, ball_in_pin_basis)  # in pinframe

        return normal
