from components_impl import set_btn, Touchpad, Mousewheel, LMB, RMB


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
