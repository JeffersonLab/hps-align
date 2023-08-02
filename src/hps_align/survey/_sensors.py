
import numpy as np
import warnings

from ._parser import Parser
from ._fixture import Fixture
from ._utils import *
from ._cli import app


class Sensor:

    def __init__(self, input_file=None, input_file_fixture=None):

        self.fixture = Fixture(input_file_fixture)

        if input_file is None:
            warnings.warn('No input file specified')
            self.oriball_dict = {'x': 0, 'y': 0, 'z': 0}
            self.diagball_dict = {'x': 0, 'y': 0, 'z': 0}
            self.axiball_dict = {'x': 0, 'y': 0, 'z': 0}
            self.sensor_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0}
            self.sensor_origin_dict = {'x': 0, 'y': 0, 'z': 0}
            return

        self.parser = Parser(input_file)

        self.oriball_dict = self._find_oriball()
        self.diagball_dict = self._find_diagball()
        self.axiball_dict = self._find_axiball()
        self.sensor_origin_dict = self._find_sensor_origin()
        self.sensor_plane_dict = self._find_sensor_plane()

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

    def _find_sensor_origin(self):
        """Find sensor origin coordinates in survey data file

        Returns
        -------
        sensor_origin : dict
            Dictionary of sensor origin coordinates
        """
        sensor_origin = self.parser.find_coords(
            self.parser.find_names(['Sensor origin'])['Sensor origin'] + 1)
        return sensor_origin

    def _find_sensor_plane(self):
        """Find sensor plane coordinates in survey data file

        Returns
        -------
        sensor_plane : dict
            Dictionary of sensor plane coordinates
        """
        sensor_plane = self.parser.find_coords(
            self.parser.find_names(['Sensor plane'])['Sensor plane'] + 1)
        return sensor_plane

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

    def get_sensor_origin_ballframe(self, use_matt_basis=False):
        """Get sensor origin coordinates in fixture ball frame

        Parameters
        ----------
        use_matt_basis : bool
            If True, use Matt's survey data file
        """
        if use_matt_basis:
            ball_basis, ball_origin = np.identity(3), np.zeros(3)
        else:
            ball_basis, ball_origin = self.get_ball_basis()
        origin = self.get_sensor_origin() - ball_origin
        origin = np.matmul(origin, np.linalg.inv(ball_basis))

        return origin

    def get_sensor_origin_pinframe(self, volume, use_matt_basis=False):
        """Get sensor origin coordinates in pin frame

        Parameters
        ----------
        volume : str
            "top" or "bottom"
        use_matt_basis : bool
            If True, use Matt's survey data file
        Returns
        -------
        origin : np.array
            Sensor origin coordinates in pin frame
        """
        origin = self.get_sensor_origin_ballframe(use_matt_basis)
        pin_basis, pin_origin = self.fixture.get_pin_in_ball(volume, use_matt_basis)

        origin = origin - pin_origin
        origin = np.matmul(origin, np.linalg.inv(pin_basis))

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
        return normal_vector(math.radians(self.sensor_plane_dict["xy_angle"]), math.radians(self.sensor_plane_dict["elevation"]))

    def get_sensor_normal_ballframe(self, use_matt_basis=False):
        """Get sensor origin coordinates in ball frame

        Parameters
        ----------
        use_matt_basis : bool
            If True, use Matt's survey data file
        Returns
        -------
        normal : np.array
            Normal vector to sensor plane in fixture ball frame
        """
        if use_matt_basis:
            ball_basis = np.identity(3)
        else:
            ball_basis = self.get_ball_basis()[0]
        normal = self.get_sensor_normal()
        normal = np.matmul(normal, np.linalg.inv(ball_basis))

        return normal

    def get_sensor_normal_pinframe(self, volume, use_matt_basis=False):
        """Get sensor normal vector in pin frame

        Parameters
        ----------
        volume : str
            "top" or "bottom"
        use_matt_basis : bool
            If True, use Matt's survey data file
        Returns
        -------
        normal : np.array
            Sensor normal vector in pin frame
        """
        normal = self.get_sensor_normal_ballframe(use_matt_basis)
        pin_basis = self.fixture.get_pin_in_ball(volume, use_matt_basis)[0]

        normal = np.matmul(normal, np.linalg.inv(pin_basis))

        return normal
