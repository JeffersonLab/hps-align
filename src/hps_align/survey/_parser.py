
import math
from ._cli import app


class Parser:
    """Class to parse survey data files and extract relevant information

    Parameters
    ----------
    input_file : str
        Path to survey data file

    Attributes
    ----------
    input_file : str
        Path to survey data file
    """

    def __init__(self, input_file):
        self.input_file = input_file

    def find_names(self, input_strings):
        """Find line numbers of first appearances of strings in survey data file

        Parameters
        ----------
        input_strings : list
            List of strings to search for

        Returns
        -------
        first_appearances : dict
            Dictionary of line numbers of first appearances of strings
        """
        first_appearances = {}

        with open(self.input_file, 'r') as file:
            for line_num, line in enumerate(file):
                for string in input_strings:
                    if string in line and string not in first_appearances:
                        first_appearances[string] = line_num

        return first_appearances

    def find_coords(self, line_number, num_lines_to_read=15):
        """Find coordinates in survey data file starting at line_number

        Parameters
        ----------
        line_number : int
            Line number to start reading from
        num_lines_to_read : int
            Number of lines to read from line_number

        Returns
        -------
        coordinates : dict
            Dictionary of coordinates
        """
        coordinates = {}
        with open(self.input_file, 'r') as file:
            for _ in range(line_number - 1):
                next(file)  # Skip lines until we reach the desired starting line

            for _ in range(num_lines_to_read):
                line = next(file)
                if "X Location" in line:
                    coordinates["x"] = float(line.split()[2])
                elif "Y Location" in line:
                    coordinates["y"] = float(line.split()[2])
                elif "Z Location" in line:
                    coordinates["z"] = float(line.split()[2])
                elif "XY Angle" in line:
                    coordinates["xy_angle"] = math.radians(float(line.split()[2]))
                elif "Elevation" in line:
                    coordinates["elevation"] = math.radians(float(line.split()[2]))

        return coordinates