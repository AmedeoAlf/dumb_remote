# Dumb remote

A websocket based application to control your mouse from a webui.

I made this because scrolling reddit on a trackpad for 6+ hours hurts your hand,
now I can use my phone as a mouse and rest in a more ergonomical position.

## Note on modularity

This software comes batteries included for Linux using the uinput kernel module.
It would probably be a good idea to use a more portable library (for example
pyautogui), which I didn't use due to it not working on Hyprland.

Since this isn't portable, all platform specific code (uinput) lives inside
`components_impl.py`; porting to another library is just a matter of
reimplementing `set_btn()`, `Touchpad._rel_move()`, `Mousewheel._rel_move()` and
`click()`.

## Dependencies

* [aiohttp](https://github.com/aio-libs/aiohttp) for the webui hosting and the
websocket connection
* [uinput](https://github.com/tuomasjjrasanen/python-uinput) for creating the
virtual mouse (needed only for default `components_impl.py`)

Make sure the uinput module is loaded, to load it for current boot:

```sh
sudo modprobe uinput
```

## Usage

Generate the JS code for the components

```sh
python build_templates.py
```

Run the HTTP + WS server

```sh
python server.py
```

(depending on permissions you might need to run as root)

The server should now be listening on port 8080: you can now connect from your
phone and start controlling your PC.
