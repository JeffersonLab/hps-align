from _utils import *
from _parser import Parser


class BasePlane:

    def __init__(self, input_file):
        self.input_file = input_file
        self.parser = Parser(input_file)

        self.L0_base_plane_dict = self._find_L0_base_plane()
        self.L1_base_plane_dict = self._find_L1_base_plane()
        self.L2_base_plane_dict = self._find_L2_base_plane()
        self.L3_base_plane_dict = self._find_L3_base_plane()

    def _find_L0_base_plane(self):
        """Find L0 base plane coordinates in survey data file

        Returns
        -------
        L0_base_plane : dict
            Dictionary of L0 base plane coordinates
        """
        L0_base_plane = self.parser.find_coords(
            self.parser.find_names(['L0 base plane'])['L0 base plane'] + 1)
        return L0_base_plane

    def _find_L1_base_plane(self):
        """Find L1 base plane coordinates in survey data file

        Returns
        -------
        L1_base_plane : dict
            Dictionary of L1 base plane coordinates
        """
        L1_base_plane = self.parser.find_coords(
            self.parser.find_names(['L1 base plane'])['L1 base plane'] + 1)
        return L1_base_plane

    def _find_L2_base_plane(self):
        """Find L2 base plane coordinates in survey data file

        Returns
        -------
        L2_base_plane : dict
            Dictionary of L2 base plane coordinates
        """
        L2_base_plane = self.parser.find_coords(
            self.parser.find_names(['L2 base plane'])['L2 base plane'] + 1)
        return L2_base_plane

    def _find_L3_base_plane(self):
        """Find L3 base plane coordinates in survey data file

        Returns
        -------
        L3_base_plane : dict
            Dictionary of L3 base plane coordinates
        """
        L3_base_plane = self.parser.find_coords(
            self.parser.find_names(['L3 base plane'])['L3 base plane'] + 1)
        return L3_base_plane
    
    def get_base_plane_dict(self, layer):
        """Get base plane coordinates for a given layer

        Parameters
        ----------
        layer : int
            Layer number

        Returns
        -------
        base_plane : dict
            Dictionary of base plane coordinates
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
        
        return base_plane

    def get_base_plane_origin(self, layer):
        """Get base plane origin coordinates for a given layer

        Parameters
        ----------
        layer : int
            Layer number

        Returns
        -------
        base_plane_origin : np.array
            Base plane origin coordinates
        """
        base_plane = self.get_base_plane_dict(layer)
        return np.array([base_plane['x'], base_plane['y'], base_plane['z']])

    def get_base_plane_normal(self, layer):
        """Get base plane normal vector for a given layer

        Parameters
        ----------
        layer : int
            Layer number

        Returns
        -------
        base_plane_normal : np.array
            Base plane normal vector
        """
        base_plane = self.get_base_plane_dict(layer)
        return normal_vector(base_plane['xy_angle'], base_plane['elevation'])


# if __name__ == '__main__':
#     baseplane = BasePlane('/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_empty_top_1.txt')

#     print(baseplane._find_L0_base_plane())
#     print(baseplane._find_L1_base_plane())
#     print(baseplane._find_L2_base_plane())
#     print(baseplane._find_L3_base_plane())
