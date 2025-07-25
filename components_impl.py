import uinput
from scrollable import Scrollable

LMB = uinput.BTN_LEFT
RMB = uinput.BTN_RIGHT

_device = uinput.Device([uinput.REL_X, uinput.REL_Y, uinput.REL_WHEEL_HI_RES,
                         uinput.REL_HWHEEL_HI_RES, uinput.BTN_LEFT, uinput.BTN_RIGHT])


class Touchpad(Scrollable):
    def _rel_move(self, dx: int, dy: int) -> None:
        _device.emit(uinput.REL_X, dx)
        _device.emit(uinput.REL_Y, dy)


class Mousewheel(Scrollable):
    def __init__(self) -> None:
        self.sensibility = (-12, 4)

    def _rel_move(self, dx: int, dy: int) -> None:
        _device.emit(uinput.REL_HWHEEL_HI_RES, dx)
        _device.emit(uinput.REL_WHEEL_HI_RES, dy)


def set_btn(button, pressed: bool):
    _device.emit(button, pressed)
