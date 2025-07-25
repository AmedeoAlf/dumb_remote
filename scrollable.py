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
