import numpy


def lensquared(arr):
    return arr[0] ** 2 + arr[1] ** 2


def accel_function(x):
    # assuming values [0, 60]
    return (0.015 * x ** 2) * numpy.sign(x) + x


class Scrollable:
    def __init__(self) -> None:
        self.sensibility = (1, 1)

    def finger_down(self, pos: tuple[float, float]) -> None:
        self.pos = pos

    def move_to(self, pos: tuple[float, float]) -> None:
        self._rel_move(
            int(accel_function((pos[0] - self.pos[0]) * self.sensibility[0])),
            int(accel_function((pos[1] - self.pos[1]) * self.sensibility[1])),
        )
        self.pos = pos

    def _rel_move(self, dx: int, dy: int) -> None:
        raise Exception("This is a virtual method should not be called")
