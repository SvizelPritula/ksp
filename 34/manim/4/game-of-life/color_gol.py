from manim import *

from typing import Generator, Optional, Tuple
from random import Random

from cell_field import FieldHandle
from cell_field_manim import MCellField
from keyframed_func import keyframes

# Založeno na hře GOLAD https://www.youtube.com/watch?v=JkGZ2Hl1l8c

random = Random(13370)

total_steps = 100
size = 20, 20, 20

wait_time = keyframes([
    (0, 0.3),
    (15, 0.1),
    (85, 0.1),
    (100, 0.3)
])


class Color(Enum):
    Black = 0
    Red = 1
    Blue = 2


def get_neighbours() -> Generator[Tuple[int, int, int], None, None]:
    for x in range(-1, 1 + 1):
        for y in range(-1, 1 + 1):
            for z in range(-1, 1 + 1):
                if x != 0 or y != 0 or z != 0:
                    yield x, y, z


neighbours = list(get_neighbours())


def initializer(coords: Tuple[int, int, int]) -> Color:
    if random.random() < 0.3:
        return random.choice([Color.Red, Color.Blue])
    return Color.Black


def updater(field: FieldHandle[Color]) -> Color:
    alive_neighbours = 0
    red_neighbours = 0
    blue_neighbours = 0

    for coords in neighbours:
        if field[coords] != Color.Black:
            alive_neighbours += 1
        if field[coords] == Color.Red:
            red_neighbours += 1
        if field[coords] == Color.Blue:
            blue_neighbours += 1

    if field.state != Color.Black:
        if alive_neighbours not in [4, 5]:
            return Color.Black
    else:
        if alive_neighbours in [5]:
            return Color.Red if red_neighbours > blue_neighbours else Color.Blue

    return field.state


def visualizer(field: FieldHandle[Color]) -> Optional[VMobject]:
    if field.state != Color.Black:
        color = RED if field.state == Color.Red else BLUE

        return Cube(side_length=1, fill_color=color, fill_opacity=1)
    else:
        return None


class ColorGOL(ThreeDScene):
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
