
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
            self.L0_hole_pin_dict = {'x': 0, 'y': 0, 'z': 0}
            self.L0_slot_pin_dict = {'x': 0, 'y': 0, 'z': 0}
            self.L1_hole_pin_dict = {'x': 0, 'y': 0, 'z': 0}
            self.L1_slot_pin_dict = {'x': 0, 'y': 0, 'z': 0}
            self.L2_hole_pin_dict = {'x': 0, 'y': 0, 'z': 0}
            self.L2_slot_pin_dict = {'x': 0, 'y': 0, 'z': 0}
            self.L3_hole_pin_dict = {'x': 0, 'y': 0, 'z': 0}
            self.L3_slot_pin_dict = {'x': 0, 'y': 0, 'z': 0}
            return

        self.parser = Parser(input_file)

        self.L0_hole_pin_dict = self.parser.get_coords('L0 hole pin')
        self.L0_slot_pin_dict = self.parser.get_coords('L0 slot pin')
        self.L1_hole_pin_dict = self.parser.get_coords('L1 hole pin')
        self.L1_slot_pin_dict = self.parser.get_coords('L1 slot pin')
        self.L2_hole_pin_dict = self.parser.get_coords('L2 hole pin')
        self.L2_slot_pin_dict = self.parser.get_coords('L2 slot pin')
        self.L3_hole_pin_dict = self.parser.get_coords('L3 hole pin')
        self.L3_slot_pin_dict = self.parser.get_coords('L3 slot pin')

    def set_pin(self, pin_coords, layer, pin_type):
        """Set pin coordinates to given values

        Overwrites the pin coordinates from the survey data file.

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
        """Get pin coordinates

        The coordinates are either read from survey data file or have been set manually before.

        Parameters
        ----------
        layer : int
            Layer number
        pin_type : str
            Pin type

        Returns
        -------
        pin : np.array
            Pin position in OGP (or other global) coordinates
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
