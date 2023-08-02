import warnings

from ._utils import *
from ._parser import Parser
from ._cli import app


class Pin:

    def __init__(self, input_file=None):
        """Initialize Pin object

        Parameters
        ----------
        input_file : str
            Survey data file
        """
        if input_file is None:
            warnings.warn('No input file specified')
            self.L0_hole_pin_dict = {'x': 0, 'y': 0, 'z': 0}
            self.L0_slot_pin_dict = {'x': 0, 'y': 0, 'z': 0}
            self.L1_hole_pin_dict = {'x': 0, 'y': 0, 'z': 0}
            self.L1_slot_pin_dict = {'x': 0, 'y': 0, 'z': 0}
            self.L2_hole_pin_dict = {'x': 0, 'y': 0, 'z': 0}
            self.L2_slot_pin_dict = {'x': 0, 'y': 0, 'z': 0}
            self.L3_hole_pin_dict = {'x': 0, 'y': 0, 'z': 0}
            self.L3_slot_pin_dict = {'x': 0, 'y': 0, 'z': 0}
            return

        self.input_file = input_file
        self.parser = Parser(input_file)

        self.L0_hole_pin_dict = self._find_L0_hole_pin()
        self.L0_slot_pin_dict = self._find_L0_slot_pin()
        self.L1_hole_pin_dict = self._find_L1_hole_pin()
        self.L1_slot_pin_dict = self._find_L1_slot_pin()
        self.L2_hole_pin_dict = self._find_L2_hole_pin()
        self.L2_slot_pin_dict = self._find_L2_slot_pin()
        self.L3_hole_pin_dict = self._find_L3_hole_pin()
        self.L3_slot_pin_dict = self._find_L3_slot_pin()

    def _find_L0_slot_pin(self):
        """Find L0 slot pin coordinates in survey data file

        Returns
        -------
        L0_slot_pin : dict
            Dictionary of L0 slot pin coordinates
        """
        L0_slot_pin = self.parser.find_coords(
            self.parser.find_names(['L0 slot pin'])['L0 slot pin'] + 1)
        return L0_slot_pin

    def _find_L0_hole_pin(self):
        """Find L0 hole pin coordinates in survey data file

        Returns
        -------
        L0_hole_pin : dict
            Dictionary of L0 hole pin coordinates
        """
        L0_hole_pin = self.parser.find_coords(
            self.parser.find_names(['L0 hole pin'])['L0 hole pin'] + 1)
        return L0_hole_pin

    def _find_L1_slot_pin(self):
        """Find L1 slot pin coordinates in survey data file

        Returns
        -------
        L1_slot_pin : dict
            Dictionary of L1 slot pin coordinates
        """
        L1_slot_pin = self.parser.find_coords(
            self.parser.find_names(['L1 slot pin'])['L1 slot pin'] + 1)
        return L1_slot_pin

    def _find_L1_hole_pin(self):
        """Find L1 hole pin coordinates in survey data file

        Returns
        -------
        L1_hole_pin : dict
            Dictionary of L1 hole pin coordinates
        """
        L1_hole_pin = self.parser.find_coords(
            self.parser.find_names(['L1 hole pin'])['L1 hole pin'] + 1)
        return L1_hole_pin

    def _find_L2_slot_pin(self):
        """Find L2 slot pin coordinates in survey data file

        Returns
        -------
        L2_slot_pin : dict
            Dictionary of L2 slot pin coordinates
        """
        L2_slot_pin = self.parser.find_coords(
            self.parser.find_names(['L2 slot pin'])['L2 slot pin'] + 1)
        return L2_slot_pin

    def _find_L2_hole_pin(self):
        """Find L2 hole pin coordinates in survey data file

        Returns
        -------
        L2_hole_pin : dict
            Dictionary of L2 hole pin coordinates
        """
        L2_hole_pin = self.parser.find_coords(
            self.parser.find_names(['L2 hole pin'])['L2 hole pin'] + 1)
        return L2_hole_pin

    def _find_L3_slot_pin(self):
        """Find L3 slot pin coordinates in survey data file

        Returns
        -------
        L3_slot_pin : dict
            Dictionary of L3 slot pin coordinates
        """
        L3_slot_pin = self.parser.find_coords(
            self.parser.find_names(['L3 slot pin'])['L3 slot pin'] + 1)
        return L3_slot_pin

    def _find_L3_hole_pin(self):
        """Find L3 hole pin coordinates in survey data file

        Returns
        -------
        L3_hole_pin : dict
            Dictionary of L3 hole pin coordinates
        """
        L3_hole_pin = self.parser.find_coords(
            self.parser.find_names(['L3 hole pin'])['L3 hole pin'] + 1)
        return L3_hole_pin

    def set_pin(self, pin_coords, layer, pin_type):
        """Set pin coordinates to given values; overwrite the pin coordinates from the survey data file

        Parameters
        ----------
        pin_coords : dict
            Dictionary of pin coordinates {'x': x, 'y': y, 'z': z}
        layer : int
            Layer number
        pin_type : str
            Pin type
        """
        if not isinstance(pin_coords, dict):
            raise ValueError('Invalid ball coordinate type: {}'.format(pin_coords))

        if layer == 0:
            if pin_type == 'slot':
                self.L0_slot_pin_dict = pin_coords
            elif pin_type == 'hole':
                self.L0_hole_pin_dict = pin_coords
            else:
                raise ValueError('Invalid pin type: {}'.format(pin_type))
        elif layer == 1:
            if pin_type == 'slot':
                self.L1_slot_pin_dict = pin_coords
            elif pin_type == 'hole':
                self.L1_hole_pin_dict = pin_coords
            else:
                raise ValueError('Invalid pin type: {}'.format(pin_type))
        elif layer == 2:
            if pin_type == 'slot':
                self.L2_slot_pin_dict = pin_coords
            elif pin_type == 'hole':
                self.L2_hole_pin_dict = pin_coords
            else:
                raise ValueError('Invalid pin type: {}'.format(pin_type))
        elif layer == 3:
            if pin_type == 'slot':
                self.L3_slot_pin_dict = pin_coords
            elif pin_type == 'hole':
                self.L3_hole_pin_dict = pin_coords
            else:
                raise ValueError('Invalid pin type: {}'.format(pin_type))
        else:
            raise ValueError('Invalid layer number')

    def get_pin(self, layer, pin_type):
        """Get pin coordinates from survey data file

        Parameters
        ----------
        layer : int
            Layer number
        pin_type : str
            Pin type

        Returns
        -------
        pin : np.array
            Numpy array of pin coordinates
        """
        if layer == 0:
            if pin_type == 'slot':
                pin = self.L0_slot_pin_dict
            elif pin_type == 'hole':
                pin = self.L0_hole_pin_dict
            else:
                raise ValueError('Invalid pin type: {}'.format(pin_type))
        elif layer == 1:
            if pin_type == 'slot':
                pin = self.L1_slot_pin_dict
            elif pin_type == 'hole':
                pin = self.L1_hole_pin_dict
            else:
                raise ValueError('Invalid pin type: {}'.format(pin_type))
        elif layer == 2:
            if pin_type == 'slot':
                pin = self.L2_slot_pin_dict
            elif pin_type == 'hole':
                pin = self.L2_hole_pin_dict
            else:
                raise ValueError('Invalid pin type: {}'.format(pin_type))
        elif layer == 3:
            if pin_type == 'slot':
                pin = self.L3_slot_pin_dict
            elif pin_type == 'hole':
                pin = self.L3_hole_pin_dict
            else:
                raise ValueError('Invalid pin type: {}'.format(pin_type))
        else:
            raise ValueError('Invalid layer number')

        return np.array([pin['x'], pin['y'], pin['z']])
