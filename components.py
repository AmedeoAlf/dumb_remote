from typing import Callable, Optional
from components_impl import set_btn, click, Touchpad, Mousewheel
import json

scroll_devices = {
    "mousewheel": Mousewheel(),
    "touchpad": Touchpad()
}


class EventType:
    def __init__(self, components: set[str], handler: dict[str, Callable[[list[str]], None]], js_codegen: Callable[[str, set[str], Optional[str]], str], overridden_ids: dict[str, str] = {}):
        self.components = components
        self.handler = handler
        self.js_codegen = js_codegen
        self.overridden_ids = overridden_ids

    def do_codegen(self) -> str:
        return "\n".join(map(lambda c: self.js_codegen(c, set(self.handler.keys()),
                                                       self.overridden_ids.get(c)), self.components))


def button_codegen(html_id: str, events: set[str], sent_id: Optional[str] = None) -> str:
    event_list = json.dumps(list(events))
    if sent_id != None:
        return f"broadcastEvents({json.dumps(html_id)}, {event_list}, {json.dumps(sent_id)});"
    else:
        return f"broadcastEvents({json.dumps(html_id)}, {event_list});"


def scroll_codegen(html_id: str, events: set[str], _sent_id: Optional[str] = None) -> str:
    return f"broadcastScrollEvents({json.dumps(html_id)}, {json.dumps(list(events))});"


events = [
    EventType(
        components=set(scroll_devices.keys()),
        handler={
            "touchstart": lambda cmd: scroll_devices[cmd[0]].finger_down((float(cmd[2]), float(cmd[3]))),
            "touchmove": lambda cmd: scroll_devices[cmd[0]].move_to((float(cmd[2]), float(cmd[3]))),
        },
        js_codegen=scroll_codegen
    ),
    EventType(
        components={"lmb", "rmb"},
        handler={
            "touchstart": lambda cmd: set_btn(cmd[0], True),
            "touchend": lambda cmd: set_btn(cmd[0], False)
        },
        js_codegen=button_codegen,
    ),
    EventType(
        # touchpad doesn't get called since js will send it as "lmb"
        components={"touchpad"},
        handler={
            "click": lambda cmd: click(cmd[0])},
        js_codegen=button_codegen,
        overridden_ids={"touchpad": "lmb"}
    ),
]

components: dict[str, dict[str, Callable[[list[str]], None]]] = {}

for ev in events:
    for c in ev.components:
        if c in ev.overridden_ids:
            c = ev.overridden_ids[c]
        components[c] = components.get(c, {})
        for (event, handler) in ev.handler.items():
            components[c][event] = handler

print(components)
