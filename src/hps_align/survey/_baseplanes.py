from _utils import *
from _parser import Parser


class BasePlane:

    def __init__(self, input_file):
        self.input_file = input_file
        self.parser = Parser(input_file)

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


# if __name__ == '__main__':
#     baseplane = BasePlane('/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_empty_top_1.txt')

#     print(baseplane._find_L0_base_plane())
#     print(baseplane._find_L1_base_plane())
#     print(baseplane._find_L2_base_plane())
#     print(baseplane._find_L3_base_plane())
