from math import pi
from manim import *

iterations = 10


class Ant(MovingCameraScene):
    def construct(self):
        white_squares = set()

        self.camera.frame.scale_to_fit_height(5)

        x, y = 0, 0
        direction = 0

        square_objects = dict()

        ant = SVGMobject("ant.svg")
        ant.scale_to_fit_height(0.8)
        ant.z_index = 1

        self.play(Write(ant))

        for i in range(iterations):
            is_white = (x, y) in white_squares

            if is_white:
                direction -= 1
                turn_animation = Rotate(ant, pi/2)
            else:
                direction += 1
                turn_animation = Rotate(ant, -pi/2)

            direction %= 4

            if is_white:
                white_squares.remove((x, y))

                obj = square_objects[(x, y)]

                toggle_animation = FadeOut(obj)
            else:
                white_squares.add((x, y))

                obj = Square(1.01)
                obj.set_fill(WHITE, opacity=1)
                obj.set_stroke(None, 0)
                obj.move_to(RIGHT * x + DOWN * y)

                square_objects[(x, y)] = obj

                toggle_animation = FadeIn(obj)

            if direction == 0:
                x, y = x, y - 1
            if direction == 1:
                x, y = x + 1, y
            if direction == 2:
                x, y = x, y + 1
            if direction == 3:
                x, y = x - 1, y

            self.play(turn_animation, toggle_animation)
            self.play(
                ant.animate.move_to(RIGHT * x + DOWN * y),
                self.camera.frame.animate.move_to(RIGHT * x + DOWN * y)
                # Center of ant shifts during rotation, which makes an updater hard to use
            )
