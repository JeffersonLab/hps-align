
from ._utils import *
from ._ballframe import BallFrame
from ._pinframe import PinFrame
from ._cli import app


class UChannel:
    """SVT uchannel class

    The uchannel has two volumes, top and bottom. Each volume has a ball frame and multiple pin frames.
    The PinFrame class returns the pin basis for each layer.
    This class is used to calculate the pin frame basis in the uchannel ball frame.

    Attributes
    ----------
    ballframe_top : BallFrame
        BallFrame object for top volume
    ballframe_bot : BallFrame
        BallFrame object for bottom volume
    pinframe_top : PinFrame
        PinFrame object for top volume, contains information for each layer
    pinframe_bot : PinFrame
        PinFrame object for bottom volume, contains information for each layer
    """
    def __init__(self, ballframe_top=BallFrame(),
                 ballframe_bot=BallFrame(),
                 pinframe_top=PinFrame(),
                 pinframe_bot=PinFrame()):

        self.ballframe_top = ballframe_top
        self.pinframe_top = pinframe_top
        self.ballframe_bot = ballframe_bot
        self.pinframe_bot = pinframe_bot

    def get_ball_basis(self, volume):
        """Get basis vectors and origin for ball frame

        There is only one ball frame per volume.

        Parameters
        ----------
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
            ballframe = self.ballframe_top
        elif volume == 'bottom':
            ballframe = self.ballframe_bot
        else:
            raise ValueError('Invalid volume: {}'.format(volume))

        basis, origin = ballframe.get_basis(volume)

        return basis, origin

    def get_pin_basis(self, layer, volume):
        """Get basis vectors and origin for pin frame

        There is a pin frame for each layer that is determined by the respective positions of the pins.

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

    def pin_in_ballframe(self, layer, volume):
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
        ball_basis, ball_origin = self.get_ball_basis(volume)
        # rotation of basis vectors from pin frame to ball frame
        basis = np.matmul(pin_basis, np.linalg.inv(ball_basis))

        if volume == 'top' and self.ballframe_top.__class__.__name__ == 'MattBallFrame':
            origin = pin_origin
        elif volume == 'bottom' and self.ballframe_bot.__class__.__name__ == 'MattBallFrame':
            origin = pin_origin
        else:
            # translation of origin in ball frame
            origin = pin_origin - ball_origin

        origin = np.matmul(origin, np.linalg.inv(ball_basis))

        return basis, origin
