
from ._utils import *
from ._ballframe import BallFrame
from ._pinframe import PinFrame
from ._cli import app


class UChannel:

    def __init__(self, ballframe_top=BallFrame(),
                 ballframe_bot=BallFrame(),
                 pinframe_top=PinFrame(),
                 pinframe_bot=PinFrame()):
        
        self.ballframe_top = ballframe_top
        self.pinframe_top = pinframe_top
        self.ballframe_bot = ballframe_bot
        self.pinframe_bot = pinframe_bot

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

    def pin_in_ballframe(self, layer, volume, use_matt_basis=False):
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
