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

        self.parallel_wire_dict = self._find_parallel_wire()
        self.diagonal_wire_dict = self._find_diagonal_wire()

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
