
from _utils import *
from _parser import Parser


class BallFrame:

    def __init__(self, input_file):
        self.input_file = input_file
        self.parser = Parser(input_file)

    def _find_L1_hole_ball(self):
        """Find L1 hole ball coordinates in survey data file

        Returns
        -------
        L1_hole_ball : dict
            Dictionary of L1 hole ball coordinates
        """
        L1_hole_ball = self.parser.find_coords(
            self.parser.find_names(['L1 hole ball'])['L1 hole ball'] + 1)
        return L1_hole_ball

    def _find_L1_slot_ball(self):
        """Find L1 slot ball coordinates in survey data file

        Returns
        -------
        L1_slot_ball : dict
            Dictionary of L1 slot ball coordinates
        """
        L1_slot_ball = self.parser.find_coords(
            self.parser.find_names(['L1 slot ball'])['L1 slot ball'] + 1)
        return L1_slot_ball

    def _find_L3_hole_ball(self):
        """Find L3 hole ball coordinates in survey data file

        Returns
        -------
        L3_hole_ball : dict
            Dictionary of L3 hole ball coordinates
        """
        L3_hole_ball = self.parser.find_coords(
            self.parser.find_names(['L3 hole ball'])['L3 hole ball'] + 1)
        return L3_hole_ball

    def _find_L3_slot_ball(self):
        """Find L3 slot ball coordinates in survey data file

        Returns
        -------
        L3_slot_ball : dict
            Dictionary of L3 slot ball coordinates
        """
        L3_slot_ball = self.parser.find_coords(
            self.parser.find_names(['L3 slot ball'])['L3 slot ball'] + 1)
        return L3_slot_ball

    def _find_ball_plane(self):
        """Find ball plane coordinates in survey data file

        Returns
        -------
        ball_plane : dict
            Dictionary of ball plane coordinates
        """
        ball_plane = self.parser.find_coords(
            self.parser.find_names(['Step:  8'])['Step:  8'] + 1, 20)
        return ball_plane


# if __name__ == '__main__':
#     ballframe = BallFrame('/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_empty_top_1.txt')

#     print(ballframe._find_L1_hole_ball())
#     print(ballframe._find_L1_slot_ball())
#     print(ballframe._find_L3_hole_ball())
#     print(ballframe._find_L3_slot_ball())
#     print(ballframe._find_ball_plane())
