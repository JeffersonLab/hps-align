from _utils import *
from _parser import Parser


class PinFrame:

    def __init__(self, input_file):
        self.input_file = input_file
        self.parser = Parser(input_file)

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
    


# if __name__ == '__main__':
        
#     pinframe = PinFrame('/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_empty_top_1.txt')

#     print(pinframe._find_L0_slot_pin())
#     print(pinframe._find_L0_hole_pin())
#     print(pinframe._find_L1_slot_pin())
#     print(pinframe._find_L1_hole_pin())
#     print(pinframe._find_L2_slot_pin())
#     print(pinframe._find_L2_hole_pin())
#     print(pinframe._find_L3_slot_pin())
#     print(pinframe._find_L3_hole_pin())
