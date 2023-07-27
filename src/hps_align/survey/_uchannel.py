
from _utils import *
from _ballframe import BallFrame
from _pinframe import PinFrame
from _edges import SensorEdge
from _wires import Wire


class UChannel:

    def __init__(self, input_files_empty, input_files_full):
        self.input_files_empty = input_files_empty
        self.input_files_full = input_files_full

        self.ball_frame_top = BallFrame(input_files_empty['top'])
        self.pin_frame_top = PinFrame(input_files_empty['top'])
        self.ball_frame_bot = BallFrame(input_files_empty['bottom'])
        self.pin_frame_bot = PinFrame(input_files_empty['bottom'])

        self.sensor_edge_top = SensorEdge(input_files_full['top'])
        self.wire_top = Wire(input_files_full['top'])
        self.sensor_edge_bot = SensorEdge(input_files_full['bottom'])
        self.wire_bot = Wire(input_files_full['bottom'])

    def get_ball_basis(self, volume):
        if volume == 'top':
            ball_frame = self.ball_frame_top
        elif volume == 'bottom':
            ball_frame = self.ball_frame_bot
        else:
            raise ValueError('Invalid volume: {}'.format(volume))

        basis, origin = ball_frame.get_basis(volume)
        # origin in ball frame
        origin = np.matmul(basis, origin)
        return basis, origin

    def get_pin_basis(self, layer, volume):
        if volume == 'top':
            pin_frame = self.pin_frame_top
        elif volume == 'bottom':
            pin_frame = self.pin_frame_bot
        else:
            raise ValueError('Invalid volume: {}'.format(volume))

        ball_basis, ball_origin = self.get_ball_basis(volume)
        basis, origin = pin_frame.get_basis(layer)
        # origin in ball frame
        origin = np.matmul(ball_basis, origin)
        return basis, origin

    def pin_to_ball_frame(self, layer, volume):
        """Transform pin coordinates to ball frame coordinates

        Parameters
        ----------
        layer : int
            Layer number

        Returns
        -------
        pin_to_ball : np.array
            Numpy array of pin coordinates in ball frame
        """
        pin_basis, pin_origin = self.get_pin_basis(layer)
        ball_basis, ball_origin = self.get_ball_basis(volume)

        # rotation of basis vectors from pin frame to ball frame
        rotation = np.matmul(np.linalg.inv(ball_basis), pin_basis)
        # translation of origin in ball frame
        translation = ball_origin - pin_origin

        return rotation, translation

    def pin_to_ball_vector(self, vec, layer, volume):
        """Transform vector from pin frame to ball frame

        Parameters
        ----------
        vec : np.array
            Numpy array of vector coordinates in pin frame
        layer : int
            Layer number

        Returns
        -------
        vec : np.array
            Numpy array of vector coordinates in ball frame
        """
        rotation, translation = self.pin_to_ball_frame(layer, volume)
        vec = np.matmul(rotation, vec) + translation
        return vec


if __name__ == '__main__':
    input_files_empty = {'top': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_empty_top_1.txt',
                         'bottom': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_empty_bottom_1.txt'}
    input_files_full = {'top': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_full_top_1.txt',
                        'bottom': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_full_bottom_1.txt'}

    uchannel = UChannel(input_files_empty, input_files_full)

    # print(uchannel.get_ball_basis())
    print(uchannel.get_pin_basis(2, 'top')[1])
    print(uchannel.get_pin_basis(3, 'top')[1])
    print(uchannel.get_pin_basis(2, 'bottom')[1])
    print(uchannel.get_pin_basis(3, 'bottom')[1])
    # print(uchannel.pin_to_ball_frame(2))
    # print(uchannel.pin_to_ball_vector(np.array([0, 0, 0]), 2))
