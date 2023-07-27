from _utils import *

from _pins import Pin
from _baseplanes import BasePlane


class PinFrame:

    def __init__(self, input_file):
        self.input_file = input_file
        self.pins = Pin(input_file)
        self.base_planes = BasePlane(input_file)

    def get_basis(self, layer):
        """Get basis vectors for pin frame
        
        Parameters
        ----------
        layer : int
            Layer number
        
        Returns
        -------
        basis : np.array
            Numpy array of basis vectors
        hole_pin_projected : np.array
            Origin coordinates
        """
        hole_pin = self.pins.get_pin(layer, 'hole')
        slot_pin = self.pins.get_pin(layer, 'slot')
        plane_origin = self.base_planes.get_base_plane_origin(layer)
        plane_normal = self.base_planes.get_base_plane_normal(layer)

        hole_pin_projected = project_to_plane(hole_pin, plane_origin, plane_normal)
        slot_pin_projected = project_to_plane(slot_pin, plane_origin, plane_normal)

        hole_to_slot = slot_pin_projected - hole_pin_projected
        basis = make_basis(hole_to_slot, plane_normal)

        return basis, hole_pin_projected


# if __name__ == '__main__':

#     pinframe = PinFrame('/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_empty_top_1.txt')

