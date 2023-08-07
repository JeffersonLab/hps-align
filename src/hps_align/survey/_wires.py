import warnings

from ._utils import *
from ._parser import Parser
from ._cli import app


class Wire:

    def __init__(self, input_file=None):
        """Initialize Wire object

        Parameters
        ----------
        input_file : str
            Survey data file
        """
        if input_file is None:
            warnings.warn('No input file specified')
            self.parallel_wire_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0}
            self.diagonal_wire_dict = {'x': 0, 'y': 0, 'z': 0, 'xy_angle': 0, 'elevation': 0}
            return

        self.input_file = input_file
        self.parser = Parser(input_file)

        self.parallel_wire_dict = self.parser.get_coords('Parallel wire')
        self.diagonal_wire_dict = self.parser.get_coords('Diagonal wire')
