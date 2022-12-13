from manim import *

from typing import Generator, Optional, Tuple
from random import Random

from cell_field import FieldHandle
from cell_field_manim import MCellField
from keyframed_func import keyframes


random = Random(1337)

total_steps = 100
size = 10, 10, 10

wait_time = keyframes([
    (0, 0.3),
    (15, 0.1),
    (85, 0.1),
    (100, 0.3)
])

max_liveliness = 10


def get_neighbours() -> Generator[Tuple[int, int, int], None, None]:
    for x in range(-1, 1 + 1):
        for y in range(-1, 1 + 1):
            for z in range(-1, 1 + 1):
                if x != 0 or y != 0 or z != 0:
                    yield x, y, z


neighbours = list(get_neighbours())


def initializer(coords: Tuple[int, int, int]) -> int:
    if random.random() < 0.3:
        return random.randint(1, max_liveliness)
    else:
        return 0


def updater(field: FieldHandle[int]) -> int:
    alive_neighbours = 0

    for coords in neighbours:
        if field[coords] > 0:
            alive_neighbours += 1

    if field.state >= 1:
        if field.state == 1 and alive_neighbours not in [2, 6, 9]:
            return 0
        return max(field.state - 1, 1)

    else:
        if alive_neighbours in [4, 6, 8, 9]:
            return max_liveliness
        return 0


def visualizer(field: FieldHandle[int]) -> Optional[VMobject]:
    if field.state > 0:
        frac_liveliness = field.state / max_liveliness

        size = 0.5 + 0.5 * frac_liveliness
        color = rgb_to_color((1, frac_liveliness, frac_liveliness))

        return Cube(side_length=size, fill_color=color, fill_opacity=1)
    else:
        return None


class LivelinessGOL(ThreeDScene):
    def construct(self):
        field = MCellField(size, initializer)
        field.set_visualizer(visualizer)

        self.set_camera_orientation(phi=75*DEGREES, theta=30*DEGREES, zoom=0.3)
        self.begin_ambient_camera_rotation(rate=0.15)

        self.play(FadeIn(field))

        for i in range(total_steps):
            self.wait(wait_time(i))

            field.tick(updater)

        self.wait(wait_time(total_steps))
        self.play(FadeOut(field))
