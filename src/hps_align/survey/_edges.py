from _utils import *
from _parser import Parser


class SensorEdge:

    def __init__(self, input_file):
        self.input_file = input_file
        self.parser = Parser(input_file)

    def _find_L0_axial_frontedge(self):
        """Find L0 axial front edge coordinates in survey data file
        
        Returns
        -------
        L0_axial_frontedge : dict
            Dictionary of L0 axial front edge coordinates
        """
        L0_axial_frontedge = self.parser.find_coords(
            self.parser.find_names(['L0 axial front edge'])['L0 axial front edge'] + 1)
        return L0_axial_frontedge
    
    def _find_L0_stereo_backedge(self):
        """Find L0 stereo back edge coordinates in survey data file
        
        Returns
        -------
        L0_stereo_backedge : dict
            Dictionary of L0 stereo back edge coordinates
        """
        L0_stereo_backedge = self.parser.find_coords(
            self.parser.find_names(['L0 stereo back edge'])['L0 stereo back edge'] + 1)
        return L0_stereo_backedge
    
    def _find_L1_axial_frontedge(self):
        """Find L1 axial front edge coordinates in survey data file
        
        Returns
        -------
        L1_axial_frontedge : dict
            Dictionary of L1 axial front edge coordinates
        """
        L1_axial_frontedge = self.parser.find_coords(
            self.parser.find_names(['L1 axial front edge'])['L1 axial front edge'] + 1)
        return L1_axial_frontedge
    
    def _find_L1_stereo_backedge(self):
        """Find L1 stereo back edge coordinates in survey data file
        
        Returns
        -------
        L1_stereo_backedge : dict
            Dictionary of L1 stereo back edge coordinates
        """
        L1_stereo_backedge = self.parser.find_coords(
            self.parser.find_names(['Step:  51'])['Step:  51'] + 1, 20)
        return L1_stereo_backedge
    
    def _find_L2_axial_frontedge(self):
        """Find L2 axial front edge coordinates in survey data file
        
        Returns
        -------
        L2_axial_frontedge : dict
            Dictionary of L2 axial front edge coordinates
        """
        L2_axial_frontedge = self.parser.find_coords(
            self.parser.find_names(['L2 axial front edge'])['L2 axial front edge'] + 1)
        return L2_axial_frontedge
    
    def _find_L2_stereo_backedge(self):
        """Find L2 stereo back edge coordinates in survey data file
        
        Returns
        -------
        L2_stereo_backedge : dict
            Dictionary of L2 stereo back edge coordinates
        """
        L2_stereo_backedge = self.parser.find_coords(
            self.parser.find_names(['L2 stereo back edge'])['L2 stereo back edge'] + 1)
        return L2_stereo_backedge
    
    def _find_L3_axial_frontedge(self):
        """Find L3 axial front edge coordinates in survey data file
        
        Returns
        -------
        L3_axial_frontedge : dict
            Dictionary of L3 axial front edge coordinates
        """
        L3_axial_frontedge = self.parser.find_coords(
            self.parser.find_names(['L3 axial front edge'])['L3 axial front edge'] + 1)
        return L3_axial_frontedge
    
    def _find_L3_stereo_backedge(self):
        """Find L3 stereo back edge coordinates in survey data file
        
        Returns
        -------
        L3_stereo_backedge : dict
            Dictionary of L3 stereo back edge coordinates
        """
        L3_stereo_backedge = self.parser.find_coords(
            self.parser.find_names(['L3 stereo back edge'])['L3 stereo back edge'] + 1)
        return L3_stereo_backedge
    

# if __name__ == '__main__':
#     edge = SensorEdge('/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_full_top_1.txt')

#     print(edge._find_L0_axial_frontedge())
#     print(edge._find_L0_stereo_backedge())
#     print(edge._find_L1_axial_frontedge())
#     print(edge._find_L1_stereo_backedge())
#     print(edge._find_L2_axial_frontedge())
#     print(edge._find_L2_stereo_backedge())
#     print(edge._find_L3_axial_frontedge())
#     print(edge._find_L3_stereo_backedge())
