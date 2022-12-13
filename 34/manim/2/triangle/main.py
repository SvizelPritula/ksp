from manim import *
from math import sqrt
import random
import uuid
import numpy

random.seed(uuid.getnode())


def make_line_updater(a: Mobject, b: Mobject):
    def line_updater(line: Line, dt):
        line.put_start_and_end_on(a.get_center(), b.get_center())

    return line_updater


def make_circle_updater(a: Mobject, b: Mobject, c: Mobject):
    def circle_updater(circle: Circle, dt):
        circle.become(Circle.from_three_points(
            a.get_center(), b.get_center(), c.get_center()))

    return circle_updater


def make_label_updater(object: Mobject, origin_objects: List[Mobject]):
    def label_updater(label: Mobject, dt):
        origin_points = np.array([o.get_center() for o in origin_objects])
        origin = numpy.average(origin_points, axis=0)
        point = object.get_center()

        vector = point - origin
        vector /= np.linalg.norm(vector)

        label.move_to(point + vector * 0.5)

    return label_updater


class Triangle(Scene):
    def construct(self):
        a, b, c = dots = [Dot(radius=0.1, z_index=1) for _ in range(3)]
        lineA, lineB, lineC = lines = [
            Line().set_stroke(YELLOW) for _ in range(3)]
        circle = Circle().set_stroke(RED)
        labelA, labelB, labelC = labels = [
            Text(t, font_size=42) for t in ["A", "B", "C"]]

        a.move_to(0 * RIGHT + 2 * UP)
        b.move_to(sqrt(3) * RIGHT + -1 * UP)
        c.move_to(-sqrt(3) * RIGHT + -1 * UP)

        lineA.add_updater(make_line_updater(a, b), call_updater=True)
        lineB.add_updater(make_line_updater(b, c), call_updater=True)
        lineC.add_updater(make_line_updater(c, a), call_updater=True)

        circle.add_updater(make_circle_updater(a, b, c), call_updater=True)

        labelA.add_updater(make_label_updater(a, dots), call_updater=True)
        labelB.add_updater(make_label_updater(b, dots), call_updater=True)
        labelC.add_updater(make_label_updater(c, dots), call_updater=True)

        self.play(AnimationGroup(*(Write(o)
                  for o in (dots+labels+lines+[circle])), lag_ratio=0.1))

        for _ in range(10):
            self.play(
                a.animate(run_time=1).move_to(
                    RIGHT * random.uniform(-1.5, 1.5) + UP * random.uniform(0.25, 3.25)),
                b.animate(run_time=1).move_to(
                    RIGHT * random.uniform(0.25, 3.25) + UP * random.uniform(-3.25, -0.25)),
                c.animate(run_time=1).move_to(
                    RIGHT * random.uniform(-3.25, -0.25) + UP * random.uniform(-3.25, -0.25))
            )

        self.play(AnimationGroup(*(Unwrite(o)
                  for o in ([circle]+lines+labels+dots)), lag_ratio=0.1))
