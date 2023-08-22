
import numpy as np
import warnings

from ._parser import Parser
from ._fixture import *
from ._utils import *
from ._cli import app


class Sensor:

    def __init__(self, fixture, input_file=None):

        self.fixture = fixture
        if input_file is None:
            warnings.warn('No input file specified')
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
            Array of ball coordinates
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
            Array of basis vectors
        origin : np.array
            Array of origin coordinates
        """
        origin = self.get_ball('oriball')
        basis = make_basis(self.get_ball('axiball') - origin, self.get_ball('diagball') - origin)

        return basis, origin

    def set_sensor_origin(self, sensor_origin):
        """Set sensor origin coordinates

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
            Sensor origin coordinates
        """
        return np.array([self.sensor_origin_dict['x'], self.sensor_origin_dict['y'], self.sensor_origin_dict['z']])

    def get_sensor_origin_ballframe(self):
        """Get sensor origin coordinates in fixture ball frame"""
        ball_basis, ball_origin = self.get_ball_basis()
        origin = self.get_sensor_origin() - ball_origin
        origin = np.matmul(origin, np.linalg.inv(ball_basis))

        return origin

    def get_sensor_origin_pinframe(self):
        """Get sensor origin coordinates in pin frame

        Returns
        -------
        origin : np.array
            Sensor origin coordinates in pin frame
        """
        origin = self.get_sensor_origin_ballframe()
        # print('sensor origin in fixture ballframe: ', origin)
        pin_in_ball_origin = self.fixture.get_pin_in_ball()[1]
        # print('pin in ball origin: ', pin_in_ball_origin)
        ball_in_pin_basis = self.fixture.get_ball_in_pin()[0]
        origin = origin - pin_in_ball_origin
        origin = np.matmul(origin, ball_in_pin_basis)

        return origin

    def set_sensor_plane(self, sensor_plane):
        """Set sensor plane coordinates

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
            Normal vector to sensor plane
        """
        return normal_vector(self.sensor_plane_dict["xy_angle"], self.sensor_plane_dict["elevation"])

    def get_sensor_normal_ballframe(self):
        """Get sensor origin coordinates in fixture ball frame"""
        ball_basis = self.get_ball_basis()[0]
        normal = self.get_sensor_normal()
        normal = np.matmul(normal, np.linalg.inv(ball_basis))

        return normal

    def get_sensor_normal_pinframe(self):
        """Get sensor normal vector in pin frame

        Returns
        -------
        normal : np.array
            Sensor normal vector in pin frame
        """
        normal = self.get_sensor_normal_ballframe()
        ball_in_pin_basis = self.fixture.get_ball_in_pin()[0]

        normal = np.matmul(normal, ball_in_pin_basis)

        return normal


class MattSensor(Sensor):

    def __init__(self, fixture, input_file=None):
        self.parser = None
        super().__init__(fixture, input_file)

        if self.parser:
            self.oriball_dict = self.parser.get_coords('oriball')
            self.diagball_dict = self.parser.get_coords('diagball')
            self.axiball_dict = self.parser.get_coords('axiball')
            self.ball_plane_dict = self.parser.get_coords('Step:  4', 20)
            self.sensor_origin_dict = self.parser.get_coords('Sensor origin')
            self.sensor_plane_dict = self.parser.get_coords('Sensor plane')

    def _find_sensor_active_edge_beam(self):
        """Find sensor active edge (closer to beam) coordinates in survey data file

        Returns
        -------
        sensor_active_edge : dict
            Dictionary of sensor active edge coordinates
        """
        sensor_active_edge_beam = self.parser.find_coords(
            self.parser.find_names(['Active edge beam'])['Active edge beam'] + 1)
        return sensor_active_edge_beam

    def _find_sensor_active_edge_away(self):
        """Find sensor active edge (away from beam) coordinates in survey data file

        Returns
        -------
        sensor_active_edge : dict
            Dictionary of sensor active edge coordinates
        """
        sensor_active_edge_away = self.parser.find_coords(
            self.parser.find_names(['Active edge away'])['Active edge away'] + 1)
        return sensor_active_edge_away

    def _find_sensor_physical_edge(self):
        """Find sensor physical edge coordinates in survey data file

        Returns
        -------
        sensor_physical_edge : dict
            Dictionary of sensor physical edge coordinates
        """
        sensor_physical_edge = self.parser.find_coords(
            self.parser.find_names(['Sensor physical edge'])['Sensor physical edge'] + 1)
        return sensor_physical_edge

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

    def get_sensor_origin_ballframe(self):
        """Get sensor origin coordinates in fixture ball frame"""
        origin = self.get_sensor_origin()  # in matt coords
        return np.matmul(origin, self.matt_to_ball())

    def get_sensor_normal_ballframe(self):
        """Get sensor origin coordinates in fixture ball frame"""
        normal = self.get_sensor_normal()
        return np.matmul(normal, self.matt_to_ball())

    def get_active_edge_dir(self):
        active_edge_dict = self._find_sensor_active_edge_beam()
        direction = normal_vector(active_edge_dict['xy_angle'], active_edge_dict['elevation'])
        return direction

    def get_strip_direction_ballframe(self, volume, sensor_type):
        strip_direction = self.get_active_edge_dir()
        basis = self.fixture.get_pin_in_ball()[0]
        if np.dot(strip_direction, basis[0]) < 0:
            strip_direction = -strip_direction
        return np.matmul(strip_direction, self.matt_to_ball())

    def get_strip_direction_pinframe(self, volume, sensor_type):
        strip_direction = self.get_strip_direction_ballframe(volume, sensor_type)
        ball_in_pin_basis = self.fixture.get_ball_in_pin()[0]

        return np.matmul(strip_direction, ball_in_pin_basis)

    def get_sensor_basis_pinframe(self, volume, sensor_type):
        origin = self.get_sensor_origin_pinframe()
        normal = self.get_sensor_normal_pinframe()
        strip_direction = self.get_strip_direction_pinframe(volume, sensor_type)

        basis = make_basis(normal, strip_direction)
        basis = np.array([basis[1], basis[2], basis[0]])

        return basis, origin
