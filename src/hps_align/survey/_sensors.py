
import numpy as np

from ._parser import Parser
from ._fixture import Fixture
from ._utils import *
from ._cli import app


class Sensor:
    """Get sensor data from OGP measurement files

    Parameters
    ----------
    input_file : str
        Path to sensor survey data file
    input_file_fixture : str
        Path to fixture survey data file

    Attributes
    ----------
    parser : parser
        Parser object for survey data file
    fixture : Fixture
        Fixture object ti access fixture data
    oriball_dict : dict
        Dictionary of oriball coordinates
    diagball_dict : dict
        Dictionary of diagball coordinates
    axiball_dict : dict
        Dictionary of axiball coordinates
    sensor_origin_dict : dict
        Dictionary of sensor origin coordinates
    sensor_plane_dict : dict
        Dictionary of sensor plane coordinates
    """

    def __init__(self, input_file, input_file_fixture):
        self.parser = Parser(input_file)
        self.fixture = Fixture(input_file_fixture)

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

    def get_ball_basis(self):
        """Get ball basis

        Returns
        -------
        basis : np.array
            Array of basis vectors
        origin : np.array
            Array of origin coordinates
        """
        origin = np.array([self.oriball_dict['x'], self.oriball_dict['y'], self.oriball_dict['z']])
        axiball = np.array([self.axiball_dict['x'], self.axiball_dict['y'], self.axiball_dict['z']])
        diagball = np.array([self.diagball_dict['x'], self.diagball_dict['y'], self.diagball_dict['z']])

        basis = make_basis(axiball - origin, diagball - origin)

        return basis, origin

    def get_sensor_origin(self):
        """Get sensor origin coordinates

        Returns
        -------
        origin : np.array
            Sensor origin coordinates
        """
        origin = np.array([self.sensor_origin_dict['x'], self.sensor_origin_dict['y'], self.sensor_origin_dict['z']])
        return origin

    def get_sensor_normal(self):
        """Get sensor normal vector

        Returns
        -------
        normal : np.array
            Normal vector to sensor plane
        """
        return normal_vector(self.sensor_plane_dict["xy_angle"], self.sensor_plane_dict["elevation"])

    def get_sensor_origin_pinframe(self, volume):
        """Get sensor origin coordinates in pin frame

        Parameters
        ----------
        volume : str
            "top" or "bottom"
        Returns
        -------
        origin : np.array
            Sensor origin coordinates in pin frame
        """
        origin = self.get_sensor_origin()
        pin_basis, pin_origin = self.fixture.get_pin_basis(volume)

        origin = origin - pin_origin
        origin = np.matmul(origin, np.linalg.inv(pin_basis))

        return origin

    def get_sensor_normal_pinframe(self, volume):
        """Get sensor normal vector in pin frame

        Parameters
        ----------
        volume : str
            "top" or "bottom"
        Returns
        -------
        normal : np.array
            Sensor normal vector in pin frame
        """
        normal = self.get_sensor_normal()
        pin_basis = self.fixture.get_pin_basis(volume)[0]

        normal = np.matmul(normal, np.linalg.inv(pin_basis))

        return normal
