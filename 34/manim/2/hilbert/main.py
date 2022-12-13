from math import degrees, radians
from typing_extensions import runtime
from manim import *

from hilbert import generate_curve


class Path(VMobject):
    def __init__(self, points, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.set_points_as_corners(points)


class Hilbert(MovingCameraScene):
    def construct(self):
        self.camera.frame.set(height=3)

        max_depth = 8

        for depth in range(1, max_depth + 1):
            size = (1 << depth) - 1

            path = Path(
                [p[0] * RIGHT + p[1] * DOWN for p in generate_curve(depth)])
            path.center().set_stroke(WHITE, 5)

            self.play(Write(path))

            self.clear()
            self.add(path)

            self.play(Wait(run_time=0.5))

            if depth == max_depth:
                self.play(Unwrite(path))
                break

            a_target = path.copy().shift(UL * ((size + 1) / 2))
            b_target = path.copy().shift(UR * ((size + 1) / 2))
            c_target = path.copy().rotate(radians(-90)).shift(DL * ((size + 1) / 2))
            d_target = path.copy().rotate(radians(90)).shift(DR * ((size + 1) / 2))

            a = path

            self.play(
                a.animate.become(a_target),
                self.camera.frame.animate.set(height=size * 2 + 3)
            )

            b, c, d = path.copy(), path.copy(), path.copy()

            self.play(
                AnimationGroup(
                    b.animate(runtime=0.5).become(b_target),
                    c.animate(runtime=0.5).become(c_target),
                    d.animate(runtime=0.5).become(d_target),
                    lag_ratio=0.5
                )
            )

            self.play(
                a.animate.set_stroke(GRAY_D, 2),
                b.animate.set_stroke(GRAY_D, 2),
                c.animate.set_stroke(GRAY_D, 2),
                d.animate.set_stroke(GRAY_D, 2)
            )
