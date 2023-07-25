
import numpy as np

from _parser import parser
from _utils import normal_vector
# from _cli import app


class sensor:
    """Get sensor data from OGP measurement files
    
    Parameters
    ----------
    input_file : str
        Path to survey data file
        
    Attributes
    ----------
    input_file : str
        Path to survey data file
    parser : parser
        Parser object for survey data file
    sensor_origin_dict : dict
        Dictionary of sensor origin coordinates
    sensor_plane_dict : dict
        Dictionary of sensor plane coordinates
    sensor_active_edge_dict : dict
        Dictionary of sensor active edge coordinates
    sensor_physical_edge_dict : dict
        Dictionary of sensor physical edge coordinates
    """

    def __init__(self, input_file):
        self.input_file = input_file
        self.parser = parser(input_file)
        
        self.sensor_origin_dict = self._find_sensor_origin()
        self.sensor_plane_dict = self._find_sensor_plane()
        self.sensor_active_edge_dict = self._find_sensor_active_edge()
        self.sensor_physical_edge_dict = self._find_sensor_physical_edge()

    def _find_sensor_origin(self):
        """Find sensor origin coordinates in survey data file
        
        Returns
        -------
        sensor_origin : dict
            Dictionary of sensor origin coordinates
        """
        sensor_origin = self.parser.find_coords(
            self.parser.find_names(['Sensor origin'])['Sensor origin'] + 1)
        return sensor_origin
    
    def _find_sensor_plane(self):
        """Find sensor plane coordinates in survey data file
        
        Returns
        -------
        sensor_plane : dict
            Dictionary of sensor plane coordinates
        """
        sensor_plane = self.parser.find_coords(
            self.parser.find_names(['Sensor plane'])['Sensor plane'] + 1)
        return sensor_plane
    
    def _find_sensor_active_edge(self):
        """Find sensor active edge coordinates in survey data file
        
        Returns
        -------
        sensor_active_edge : dict
            Dictionary of sensor active edge coordinates
        """
        sensor_active_edge = self.parser.find_coords(
            self.parser.find_names(['Active edge beam'])['Active edge beam'] + 1)
        return sensor_active_edge
    
    def _find_sensor_physical_edge(self):
        """Find sensor physical edge coordinates in survey data file
        
        Returns
        -------
        sensor_physical_edge : dict
            Dictionary of sensor physical edge coordinates
        """
        sensor_physical_edge = self.parser.find_coords(
            self.parser.find_names(['Sensor physical edge'])['Sensor physical edge'] + 1)
        return sensor_physical_edge
    
    def get_sensor_origin(self):
        """Get sensor origin coordinates
        
        Returns
        -------
        origin : np.array
            Sensor origin coordinates
        """
        origin = np.array([self.sensor_origin_dict['x'], self.sensor_origin_dict['y'], self.sensor_origin_dict['z']])
        return origin
    
    # def get_sensor_plane(self):
    #     return self.sensor_plane
    
    # def get_sensor_active_edge(self):
    #     return self.sensor_active_edge

    # def get_sensor_active_edge_vector(self):
    #     return _utils.normal_vector(self.sensor_active_edge_dict["xy_angle"], self.sensor_active_edge_dict["elevation"])
    
    # def get_sensor_physical_edge(self):
    #     return self.sensor_physical_edge
    
    def get_sensor_normal(self):
        """Get sensor normal vector
        
        Returns
        -------
        normal : np.array
            Normal vector to sensor plane
        """
        return normal_vector(self.sensor_plane_dict["xy_angle"], self.sensor_plane_dict["elevation"])


# if __name__ == "__main__":
#     sensor = sensor('/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L0_axial1_1.txt')

#     print(sensor.get_sensor_origin())
#     print(sensor.get_sensor_normal())
#     print(sensor.sensor_plane_dict)
#     print(sensor.sensor_active_edge_dict)
#     print(sensor.sensor_physical_edge_dict) 
