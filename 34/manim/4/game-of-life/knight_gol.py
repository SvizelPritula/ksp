from manim import *

from typing import Generator, Optional, Tuple
from random import Random

from cell_field import FieldHandle
from cell_field_manim import MCellField
from keyframed_func import keyframes


random = Random(1337)

total_steps = 100
size = 15, 15, 15

wait_time = keyframes([
    (0, 0.3),
    (15, 0.1),
    (85, 0.1),
    (100, 0.3)
])


def get_neighbours() -> Generator[Tuple[int, int, int], None, None]:
    for x in range(-2, 2 + 1):
        for y in range(-2, 2 + 1):
            for z in range(-2, 2 + 1):
                coords = [abs(x) for x in [x, y, z]]
                coords.sort()

                if coords == [0, 1, 2]:
                    yield x, y, z


neighbours = list(get_neighbours())


def initializer(coords: Tuple[int, int, int]) -> bool:
    return random.random() < 0.2


def updater(field: FieldHandle[bool]) -> bool:
    alive_neighbours = 0

    for coords in neighbours:
        if field[coords]:
            alive_neighbours += 1

    if field.state:
        if alive_neighbours not in [3, 4]:
            return False
    else:
        if alive_neighbours in [4]:
            return True

    return field.state


def visualizer(field: FieldHandle[bool]) -> Optional[VMobject]:
    if field.state:
        return Cube(side_length=1, fill_color=WHITE, fill_opacity=1)
    else:
        return None


class KnightGOL(ThreeDScene):
    def construct(self):
        field = MCellField(size, initializer)
        field.set_visualizer(visualizer)

        self.set_camera_orientation(phi=75*DEGREES, theta=30*DEGREES, zoom=0.2)
        self.begin_ambient_camera_rotation(rate=0.15)

        self.play(FadeIn(field))

        for i in range(total_steps):
            self.wait(wait_time(i))

            field.tick(updater)

        self.wait(wait_time(total_steps))
        self.play(FadeOut(field))
