from components_impl import set_btn, Touchpad, Mousewheel, LMB, RMB


class Scrollable:
    def __init__(self) -> None:
        self.sensibility = (1, 1)

    def finger_down(self, pos: tuple[float, float]) -> None:
        self.pos = pos

    def move_to(self, pos: tuple[float, float]) -> None:
        delta = [
            int((pos[i] - self.pos[i]) * self.sensibility[i]) for i in range(2)
        ]
        self._rel_move(delta[0], delta[1])
        self.pos = pos

    def _rel_move(self, dx: int, dy: int) -> None:
        raise Exception("This is a virtual method should not be called")


touchpad = Touchpad()
mousewheel = Mousewheel()

handle_scroll = {
    "touchstart": lambda component, cmd: component.finger_down((float(cmd[2]), float(cmd[3]))),
    "touchmove": lambda component, cmd: component.move_to((float(cmd[2]), float(cmd[3]))),
}

handle_click = {
    "touchstart": lambda btn: set_btn(btn, True),
    "touchend": lambda btn: set_btn(btn, False),
    "mousedown": lambda btn: set_btn(btn, True),
    "mouseup": lambda btn: set_btn(btn, False),
}

# If the event is in this set then it means the button must go down, otherwise up
press_events = {"touchstart", "mousedown"}

components = {
    "mousewheel": lambda cmd: handle_scroll[cmd[1]](mousewheel, cmd),
    "touchpad": lambda cmd: handle_scroll[cmd[1]](touchpad, cmd),
    "lmb": lambda cmd: set_btn(LMB, cmd[1] in press_events),
    "rmb": lambda cmd: set_btn(RMB, cmd[1] in press_events),
}
