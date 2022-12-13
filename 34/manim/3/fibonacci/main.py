from math import pi
from manim import *
from fibonacci import get_fibonacci_squares

square_count = 8


class Fibonacci(MovingCameraScene):
    def construct(self):
        self.camera.frame.scale_to_fit_height(2.5)

        squares = []

        for square in get_fibonacci_squares(square_count):
            obj = VGroup(
                Square(square.number),
                MathTex(f'{square.number}^2').scale_to_fit_width(
                    square.number * 0.5)
            )

            obj.shift(RIGHT * (square.left + square.right) / 2)
            obj.shift(DOWN * (square.top + square.bottom) / 2)

            squares.append(obj)

            self.play(
                FadeIn(obj, shift=[RIGHT, UP, LEFT, DOWN][square.direction]),
                self.camera.frame.animate.scale_to_fit_height(
                    2.5 * max(abs(square.top), abs(square.bottom)))
            )

        self.camera.frame.save_state()

        self.play(
            self.camera.frame.animate.scale_to_fit_height(1.5),
            *[s.animate.set_color(GRAY_C) for s in squares]
        )

        dot = Dot()
        self.play(Write(dot))

        path = TracedPath(dot.get_center)
        self.add(path)

        dot.z_index = 2
        path.z_index = 1

        self.camera.frame.add_updater(lambda c: c.move_to(dot.get_center()))
        self.add(self.camera.frame)

        for square in get_fibonacci_squares(square_count):
            origin = [
                RIGHT * square.left + DOWN * square.top,
                RIGHT * square.left + DOWN * square.bottom,
                RIGHT * square.right + DOWN * square.bottom,
                RIGHT * square.right + DOWN * square.top
            ][square.direction]

            self.play(
                self.camera.frame.animate(rate_func=linear).scale_to_fit_height(
                    1.5 * square.number),
                Rotate(dot, pi/2, about_point=origin, rate_func=linear)
            )

        self.camera.frame.clear_updaters()
        self.play(
            self.camera.frame.animate.restore()
        )

        self.wait(1)

        self.play(
            Unwrite(dot),
            Unwrite(path),
            *[Unwrite(s) for s in squares]
        )
