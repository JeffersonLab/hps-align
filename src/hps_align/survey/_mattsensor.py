
import numpy as np

from ._parser import Parser
from ._fixture import *
from ._utils import *
from ._cli import app
from ._sensors import Sensor


class MattSensor(Sensor):

    def __init__(self, fixture, input_file=None):
        self.parser = None
        super().__init__(fixture, input_file)

        if self.parser:
            # OGP coordinates
            self.oriball_dict = self.parser.get_coords('oriball')
            self.diagball_dict = self.parser.get_coords('diagball')
            self.axiball_dict = self.parser.get_coords('axiball')
            # Matt coordinates
            self.ball_plane_dict = self.parser.get_coords('Step:  4', 20)
            self.sensor_origin_dict = self.parser.get_coords('Sensor origin')
            self.sensor_plane_dict = self.parser.get_coords('Sensor plane')

    def _find_sensor_active_edge_beam(self):
        """Find sensor active edge (closer to beam) coordinates in survey data file

        Returns
        -------
        sensor_active_edge : dict
            Dictionary of sensor active edge coordinates in Matt coordinates
        """
        sensor_active_edge_beam = self.parser.find_coords(
            self.parser.find_names(['Active edge beam'])['Active edge beam'] + 1)
        return sensor_active_edge_beam

    def _find_sensor_active_edge_away(self):
        """Find sensor active edge (away from beam) coordinates in survey data file

        Returns
        -------
        sensor_active_edge : dict
            Dictionary of sensor active edge coordinates in Matt coordinates
        """
        sensor_active_edge_away = self.parser.find_coords(
            self.parser.find_names(['Active edge away'])['Active edge away'] + 1)
        return sensor_active_edge_away

    def _find_sensor_physical_edge(self):
        """Find sensor physical edge coordinates in survey data file

        Returns
        -------
        sensor_physical_edge : dict
            Dictionary of sensor physical edge coordinates in Matt coordinates
        """
        sensor_physical_edge = self.parser.find_coords(
            self.parser.find_names(['Sensor physical edge'])['Sensor physical edge'] + 1)
        return sensor_physical_edge

    def get_sensor_origin(self):
        """Get sensor origin coordinates

        Returns
        -------
        origin : np.array
            Sensor origin in Matt coordinates
        """
        return np.array([self.sensor_origin_dict['x'], self.sensor_origin_dict['y'], self.sensor_origin_dict['z']])

    def get_sensor_normal(self):
        """Get sensor normal vector

        Returns
        -------
        normal : np.array
            Normal vector to sensor plane in Matt coordinates
        """
        return normal_vector(self.sensor_plane_dict["xy_angle"], self.sensor_plane_dict["elevation"])

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
        vec2 = normal_vector(self.ball_plane_dict["xy_angle"], self.ball_plane_dict["elevation"])
        basis = make_basis(vec1, vec2)

        return np.array([basis[0], -basis[2], basis[1]]), origin

    def matt_to_ball(self):
        """Get transformation matrix from Matt to fixture ballframe

        This is just a rotation, no translation.

        Returns
        -------
        transformation : np.array
            Transformation matrix from Matt coordinates to fixture ballframe
        """
        ball_basis = self.get_ball_basis()[0]
        matt_basis = self.get_matt_basis()[0]

        return np.matmul(matt_basis, np.linalg.inv(ball_basis))

    def get_sensor_origin_ballframe(self):
        """Get sensor origin coordinates in fixture ballframe

        Returns
        -------
        origin : np.array
            Sensor origin in fixture ballframe
        """
        origin = self.get_sensor_origin()  # in matt coords
        return np.matmul(origin, self.matt_to_ball())

    def get_sensor_normal_ballframe(self):
        """Get sensor normal in fixture ballframe

        Returns
        -------
        normal : np.array
            Sensor normal in fixture ballframe
        """
        normal = self.get_sensor_normal()  # in matt coords
        return np.matmul(normal, self.matt_to_ball())

    def get_active_edge_dir(self):
        """Get sensor active edge direction in matt coordinates

        Returns
        -------
        direction : np.array
            Sensor active edge direction in Matt coordinates
        """
        active_edge_dict = self._find_sensor_active_edge_beam()  # in matt coords
        direction = normal_vector(active_edge_dict['xy_angle'], active_edge_dict['elevation'])
        return direction

    def get_strip_direction_ballframe(self):
        """Get sensor strip direction in fixture ballframe

        Returns
        -------
        direction : np.array
            Sensor strip direction in fixture ballframe
        """
        strip_direction = self.get_active_edge_dir()  # in matt coords
        strip_direction = np.matmul(strip_direction, self.matt_to_ball())  # in fixture ballframe
        basis = self.fixture.get_pin_in_ball()[0]  # in fixture ballframe
        # basis x vector points away from slot pin
        if np.dot(strip_direction, basis[0]) < 0:
            # strip direction needs to point away from slot pin
            strip_direction = -strip_direction
        return strip_direction

    def get_strip_direction_pinframe(self):
        """Get sensor strip direction in fixture pinframe

        Returns
        -------
        direction : np.array
            Sensor strip direction in fixture pinframe
        """
        strip_direction = self.get_strip_direction_ballframe()  # in fixture ballframe
        ball_in_pin_basis = self.fixture.get_ball_in_pin()[0]  # ball to pin

        return np.matmul(strip_direction, ball_in_pin_basis)

    def get_sensor_basis_pinframe(self):
        """Get sensor basis vectors in fixture pinframe

        Returns
        -------
        basis : np.array
            Sensor basis vectors in fixture pinframe
        origin : np.array
            Sensor origin in fixture pinframe
        """
        origin = self.get_sensor_origin_pinframe()  # in fixture pinframe
        normal = self.get_sensor_normal_pinframe()  # in fixture pinframe
        strip_direction = self.get_strip_direction_pinframe()  # in fixture pinframe

        basis = make_basis(normal, strip_direction)
        basis = np.array([basis[1], basis[2], basis[0]])

        return basis, origin
