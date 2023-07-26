
from _utils import *
from _ballframe import BallFrame
from _pinframe import PinFrame
from _baseplanes import BasePlane
from _edges import SensorEdge
from _wires import Wire


class UChannel:

    def __init__(self, input_file_empty, input_file_full):
        self.input_file_full = input_file_empty
        self.input_file_empty = input_file_full

        self.ball_frame = BallFrame(input_file_empty)
        self.pin_frame = PinFrame(input_file_empty)
        self.base_planes = BasePlane(input_file_empty)

        self.sensor_edge = SensorEdge(input_file_full)
        self.wire = Wire(input_file_full)
