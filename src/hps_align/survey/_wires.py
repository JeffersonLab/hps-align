from _utils import *
from _parser import Parser


class Wire:

    def __init__(self, input_file):
        self.input_file = input_file
        self.parser = Parser(input_file)

    def _find_parallel_wire(self):
        """Find parallel wire coordinates in survey data file
        
        Returns
        -------
        parallel_wire : dict
            Dictionary of parallel wire coordinates
        """
        parallel_wire = self.parser.find_coords(
            self.parser.find_names(['Parallel wire'])['Parallel wire'] + 1)
        return parallel_wire
    
    def _find_diagonal_wire(self):
        """Find diagonal wire coordinates in survey data file
        
        Returns
        -------
        diagonal_wire : dict
            Dictionary of diagonal wire coordinates
        """
        diagonal_wire = self.parser.find_coords(
            self.parser.find_names(['Diagonal wire'])['Diagonal wire'] + 1)
        return diagonal_wire
    

# if __name__ == '__main__':
#     wire = Wire('/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_full_top_1.txt')

#     print(wire._find_parallel_wire())
#     print(wire._find_diagonal_wire())
