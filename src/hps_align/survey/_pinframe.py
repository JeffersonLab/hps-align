
from ._utils import *
from ._pins import Pin
from ._baseplanes import BasePlane
from ._cli import app


class PinFrame:
    """SVT uchannel pin frame class

    Gets pin positions from survey data file and calculates basis vectors and origin
    using the BasePlane and Pin classes.

    Attributes
    ----------
    input_file : str
        Survey data file
    pins : Pin
        Pin object, uses input_file to get pin coordinates
    base_planes : BasePlane
        BasePlane object, uses input_file to get base plane coordinates
    """
    def __init__(self, input_file=None):
        """Initialize PinFrame object

        Parameters
        ----------
        input_file : str
            Survey data file
        """
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
            Basis vectors in OGP (or other global) coordinates
        hole_pin_projected : np.array
            Origin in OGP (or other global) coordinates
        """
        hole_pin = self.pins.get_pin(layer, 'hole')
        slot_pin = self.pins.get_pin(layer, 'slot')
        plane_origin, plane_normal = self.base_planes.get_base_plane(layer)

        hole_pin_projected = project_to_plane(hole_pin, plane_origin, plane_normal)
        slot_pin_projected = project_to_plane(slot_pin, plane_origin, plane_normal)

        slot_to_hole = hole_pin_projected - slot_pin_projected
        basis = make_basis(slot_to_hole, plane_normal)

        return basis, hole_pin_projected
