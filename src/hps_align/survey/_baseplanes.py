
from ._utils import *
from ._parser import Parser
from ._cli import app


class BasePlane:

    def __init__(self, input_file=None):
        """Initialize BasePlane object

        Parameters
        ----------
        input_file : str
            Survey data file
        """
        if input_file is None:
            self.L0_base_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0}
            self.L1_base_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0}
            self.L2_base_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0}
            self.L3_base_plane_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0}
            return

        self.parser = Parser(input_file)
        self.L0_base_plane_dict = self.parser.get_coords('L0 base plane')
        self.L1_base_plane_dict = self.parser.get_coords('L1 base plane')
        self.L2_base_plane_dict = self.parser.get_coords('L2 base plane')
        self.L3_base_plane_dict = self.parser.get_coords('L3 base plane')

    def set_base_plane_dict(self, base_plane_coords, layer):
        """Set base plane coordinates for a given layer

        Overwrites the pin coordinates from the survey data file.

        Parameters
        ----------
        base_plane_coords : dict
            Dictionary of base plane coordinates
        layer : int
            Layer number
        """
        if not isinstance(base_plane_coords, dict):
            raise TypeError('Base plane coordinates must be a dictionary')
        if layer == 0:
            self.L0_base_plane_dict = base_plane_coords
        elif layer == 1:
            self.L1_base_plane_dict = base_plane_coords
        elif layer == 2:
            self.L2_base_plane_dict = base_plane_coords
        elif layer == 3:
            self.L3_base_plane_dict = base_plane_coords
        else:
            raise ValueError('Invalid layer number')

    def get_base_plane(self, layer):
        """Get base plane origin coordinates and normal vector for a given layer

        The coordinates are either read from survey data file or have been set manually before.

        Parameters
        ----------
        layer : int
            Layer number

        Returns
        -------
        origin : np.array
            Base plane origin coordinates
        normal : np.array
            Base plane normal vector
        """
        if layer == 0:
            base_plane = self.L0_base_plane_dict
        elif layer == 1:
            base_plane = self.L1_base_plane_dict
        elif layer == 2:
            base_plane = self.L2_base_plane_dict
        elif layer == 3:
            base_plane = self.L3_base_plane_dict
        else:
            raise ValueError('Invalid layer number')

        origin = np.array([base_plane['x'], base_plane['y'], base_plane['z']])
        normal = normal_vector(base_plane['xy_angle'], base_plane['elevation'])

        return origin, normal
