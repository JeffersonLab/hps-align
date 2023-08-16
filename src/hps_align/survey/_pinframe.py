
import warnings

from ._utils import *
from ._pins import Pin
from ._baseplanes import BasePlane
from ._cli import app


class PinFrame:

    def __init__(self, input_file=None):
        """Initialize PinFrame object

        Parameters
        ----------
        input_file : str
            Survey data file
        """
        if input_file is None:
            warnings.warn('No input file specified')

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

        slot_to_hole = hole_pin_projected - slot_pin_projected
        basis = make_basis(slot_to_hole, plane_normal)

        return basis, hole_pin_projected
