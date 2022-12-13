import colour
from manim import *

import numpy

from solve import read_maze_from_file, solve


class Maze(Scene):
    def construct(self):
        maze, origin = read_maze_from_file("maze.txt")
        distances = solve(maze, origin)

        distance_map = dict()

        group = VGroup()

        max_distance = distances.max()
        animation_duration = 5 / max_distance

        for i, value in numpy.ndenumerate(maze):
            square = Square(side_length=.2).set_stroke(WHITE, 1, 1)

            if value:
                square.set_fill(colour.hsl2hex(
                    (distances[i] / max_distance, 1, 0.5)), 0)

                distance_map[square] = distances[i]
            else:
                square.set_fill(WHITE, 1)

            group.add(square)

        group.arrange_in_grid(rows=maze.shape[0], cols=maze.shape[1], buff=0)

        self.play(FadeIn(group))

        self.play(*map(lambda square:
                       Succession(
                           Wait(animation_duration * distance_map[square]),
                           square.animate.set_fill(square.get_fill_color(), 1)
                       ), filter(lambda square: square in distance_map, group)))

        self.play(Wait())

        self.play(FadeOut(group))
