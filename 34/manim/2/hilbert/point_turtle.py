directions: list[tuple[int, int]] = [
    [1, 0],
    [0, 1],
    [-1, 0],
    [0, -1]
]


class PointTurtle:
    def __init__(self) -> None:
        self.points: list[tuple[int, int]] = [(0, 0)]
        self.direction = 0
        self.fliped = False

    def flip(self) -> None:
        self.fliped = not self.fliped

    def rotate(self, direction: int) -> None:
        if self.fliped:
            direction = -direction

        self.direction += direction
        self.direction %= len(directions)

    def forward(self, steps: int = 1) -> None:
        direction = directions[self.direction]
        direction = direction[0] * steps, direction[1] * steps

        point = self.points[-1]
        point = point[0] + direction[0], point[1] + direction[1]

        self.points.append(point)

    def left(self) -> None:
        self.rotate(-1)

    def right(self) -> None:
        self.rotate(1)
