import uinput
from time import sleep

from scrollable import Scrollable

_device = uinput.Device([uinput.REL_X, uinput.REL_Y, uinput.REL_WHEEL_HI_RES,
                         uinput.REL_HWHEEL_HI_RES, uinput.BTN_LEFT, uinput.BTN_RIGHT])

_buttons = {
    "lmb": uinput.BTN_LEFT,
    "rmb": uinput.BTN_RIGHT,
}


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


def set_btn(button: str, pressed: bool):
    if button not in _buttons:
        return
    _device.emit(_buttons[button], pressed)


def click(button: str):
    set_btn(button, True)
    set_btn(button, False)
    # _device.emit_click(button) # does not work


fn_buttons = {
    "arrow_back": lambda: print("go back"),
    "arrow_forwards": lambda: print("go forwards"),
    "next_tab": lambda: print("next_tab"),
    "previous_tab": lambda: print("previous_tab"),
    "close_tab": lambda: print("close_tab"),
    "duplicate_tab": lambda: print("duplicate_tab"),
    "esc_btn": lambda: print("esc_btn"),
}
