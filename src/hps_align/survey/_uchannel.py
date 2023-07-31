
import warnings

from ._utils import *
from ._ballframe import BallFrame
from ._pinframe import PinFrame
from ._edges import SensorEdge
from ._wires import Wire
from ._cli import app


class UChannel:

    def __init__(self, input_files_empty=None, input_files_full=None):
        """Initialize U-channel object

        Parameters
        ----------
        input_files_empty : dict
            Dictionary of input files for empty uchannel, with keys 'top' and 'bottom'
        input_files_full : dict
            Dictionary of input files for full uchannel, with keys 'top' and 'bottom'
        """
        if input_files_empty is None:
            warnings.warn('No input files for empty uchannel specified')
            self.input_files_empty = None
            self.ballframe_top = BallFrame()
            self.pinframe_top = PinFrame()
            self.ballframe_bot = BallFrame()
            self.pinframe_bot = PinFrame()
        else:
            self.input_files_empty = input_files_empty
            self.ballframe_top = BallFrame(input_files_empty['top'])
            self.pinframe_top = PinFrame(input_files_empty['top'])
            self.ballframe_bot = BallFrame(input_files_empty['bottom'])
            self.pinframe_bot = PinFrame(input_files_empty['bottom'])

        if input_files_full is None:
            warnings.warn('No input files for full uchannel specified')
            self.input_files_full = input_files_full
            self.sensor_edge_top = SensorEdge()
            self.wire_top = Wire()
            self.sensor_edge_bot = SensorEdge()
            self.wire_bot = Wire()
        else:
            self.sensor_edge_top = SensorEdge(input_files_full['top'])
            self.wire_top = Wire(input_files_full['top'])
            self.sensor_edge_bot = SensorEdge(input_files_full['bottom'])
            self.wire_bot = Wire(input_files_full['bottom'])

    def get_ball_basis(self, volume, use_matt_basis=False):
        """Get basis vectors and origin for ball frame

        Parameters
        ----------
        volume : str
            Volume ('top' or 'bottom')
        use_matt_basis : bool
            Use Matt's basis vectors and origin (default: False);
            This is used when using Matt's OGP measurements for the empty UChannel
            that change coordinate systems halfway through

        Returns
        -------
        basis : np.array
            Numpy array of basis vectors
        origin : np.array
            Numpy array of origin coordinates
        """
        if volume == 'top':
            ball_frame = self.ballframe_top
        elif volume == 'bottom':
            ball_frame = self.ballframe_bot
        else:
            raise ValueError('Invalid volume: {}'.format(volume))

        basis, origin = ball_frame.get_basis(use_matt_basis, volume)

        return basis, origin

    def get_pin_basis(self, layer, volume):
        """Get basis vectors and origin for pin frame

        Parameters
        ----------
        layer : int
            Layer number
        volume : str
            Volume ('top' or 'bottom')

        Returns
        -------
        basis : np.array
            Numpy array of basis vectors
        origin : np.array
            Numpy array of origin coordinates
        """
        if volume == 'top':
            pin_frame = self.pinframe_top
        elif volume == 'bottom':
            pin_frame = self.pinframe_bot
        else:
            raise ValueError('Invalid volume: {}'.format(volume))

        basis, origin = pin_frame.get_basis(layer)
        return basis, origin

    def pin_in_ball_frame(self, layer, volume, use_matt_basis=False):
        """Transform pin coordinates to ball frame coordinates

        Parameters
        ----------
        layer : int
            Layer number
        volume : str
            Volume ('top' or 'bottom')

        Returns
        -------
        pin_to_ball : np.array
            Numpy array of pin coordinates in ball frame
        """
        pin_basis, pin_origin = self.get_pin_basis(layer, volume)
        ball_basis, ball_origin = self.get_ball_basis(volume, use_matt_basis)
        inv_ball_basis = np.linalg.inv(ball_basis)
        # rotation of basis vectors from pin frame to ball frame
        basis = np.matmul(inv_ball_basis, pin_basis)

        if use_matt_basis:
            origin = pin_origin
        else:
            # translation of origin in ball frame
            origin = pin_origin - ball_origin

        origin = np.matmul(origin, inv_ball_basis)

        return basis, origin


# if __name__ == '__main__':
#     input_files_empty = {'top': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_empty_top_1.txt',
#                          'bottom': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_empty_bottom_1.txt'}
#     input_files_full = {'top': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_full_top_1.txt',
#                         'bottom': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_full_bottom_1.txt'}

#     uchannel = UChannel(input_files_empty, input_files_full)

#     print(uchannel.get_pin_basis(2, 'top')[1])
#     print(uchannel.get_pin_basis(3, 'top')[1])
#     print(uchannel.get_pin_basis(2, 'bottom')[1])
#     print(uchannel.get_pin_basis(3, 'bottom')[1])
