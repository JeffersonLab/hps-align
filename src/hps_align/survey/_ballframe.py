
from _utils import *
from _parser import Parser


class BallFrame:

    def __init__(self, input_file):
        self.input_file = input_file
        self.parser = Parser(input_file)

        self.L1_hole_ball_dict = self._find_L1_hole_ball()
        self.L1_slot_ball_dict = self._find_L1_slot_ball()
        self.L3_hole_ball_dict = self._find_L3_hole_ball()
        self.L3_slot_ball_dict = self._find_L3_slot_ball()

    def _find_L1_hole_ball(self):
        """Find L1 hole ball coordinates in survey data file

        Returns
        -------
        L1_hole_ball : dict
            Dictionary of L1 hole ball coordinates
        """
        if self.parser.find_names(['L1 hole ball']):
            first_line = self.parser.find_names(['L1 hole ball'])['L1 hole ball']
        else:
            first_line = self.parser.find_names(['L1 Hole Ball'])['L1 Hole Ball'] + 1
        L1_hole_ball = self.parser.find_coords(first_line)
        return L1_hole_ball

    def _find_L1_slot_ball(self):
        """Find L1 slot ball coordinates in survey data file

        Returns
        -------
        L1_slot_ball : dict
            Dictionary of L1 slot ball coordinates
        """
        if self.parser.find_names(['L1 slot ball']):
            first_line = self.parser.find_names(['L1 slot ball'])['L1 slot ball']
        else:
            first_line = self.parser.find_names(['L1 Slot Ball'])['L1 Slot Ball'] + 1
        L1_slot_ball = self.parser.find_coords(first_line)
        return L1_slot_ball

    def _find_L3_hole_ball(self):
        """Find L3 hole ball coordinates in survey data file

        Returns
        -------
        L3_hole_ball : dict
            Dictionary of L3 hole ball coordinates
        """
        if self.parser.find_names(['L3 hole ball']):
            first_line = self.parser.find_names(['L3 hole ball'])['L3 hole ball']
        else:
            first_line = self.parser.find_names(['L3 Hole Ball'])['L3 Hole Ball'] + 1
        L3_hole_ball = self.parser.find_coords(first_line)
        return L3_hole_ball

    def _find_L3_slot_ball(self):
        """Find L3 slot ball coordinates in survey data file

        Returns
        -------
        L3_slot_ball : dict
            Dictionary of L3 slot ball coordinates
        """
        if self.parser.find_names(['L3 slot ball']):
            first_line = self.parser.find_names(['L3 slot ball'])['L3 slot ball']
        else:
            first_line = self.parser.find_names(['L3 Slot Ball'])['L3 Slot Ball'] + 1
        L3_slot_ball = self.parser.find_coords(first_line)
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

    def get_ball(self, layer, ball_type):
        """Get ball coordinates for a given layer and ball type

        Parameters
        ----------
        layer : int
            Layer number
        ball_type : str
            Ball type ('hole' or 'slot')

        Returns
        -------
        ball : np.array
            Numpy array of ball coordinates
        """
        if layer == 1:
            if ball_type == 'hole':
                ball = self.L1_hole_ball_dict
            elif ball_type == 'slot':
                ball = self.L1_slot_ball_dict
            else:
                raise ValueError('Invalid ball type: {}'.format(ball_type))
        elif layer == 3:
            if ball_type == 'hole':
                ball = self.L3_hole_ball_dict
            elif ball_type == 'slot':
                ball = self.L3_slot_ball_dict
            else:
                raise ValueError('Invalid ball type: {}'.format(ball_type))
        else:
            raise ValueError('Invalid layer: {}'.format(layer))

        return np.array([ball['x'], ball['y'], ball['z']])

    def get_basis(self, volume):
        """Get basis vectors for ball frame

        Returns
        -------
        basis : np.array
            Numpy array of basis vectors
        origin : np.array
            Origin coordinates
        """
        origin = self.get_ball(1, 'slot')
        hole_avg = (self.get_ball(1, 'hole') + self.get_ball(3, 'hole')) / 2
        basis = make_basis(self.get_ball(3, 'slot') - origin, origin - hole_avg)

        if volume == 'top':
            return np.array([-basis[0], basis[2], basis[1]]), origin
        elif volume == 'bottom':
            return np.array([basis[0], basis[2], -basis[1]]), origin
        else:
            raise ValueError('Invalid volume: {}'.format(volume))


# if __name__ == '__main__':
#     ballframe = BallFrame('/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_empty_top_1.txt')

#     print(ballframe._find_L1_hole_ball())
#     print(ballframe._find_L1_slot_ball())
#     print(ballframe._find_L3_hole_ball())
#     print(ballframe._find_L3_slot_ball())
#     print(ballframe._find_ball_plane())
