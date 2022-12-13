from colour import hsl2hex
from manim import *
import random

random.seed("Benjamin")


class Shuffle(Scene):
    def construct(self):
        self.count = 20

        self.create_circles()
        self.shuffle()
        self.destroy_circles()

    def create_circles(self):
        self.camera.frame_width = self.count * 3
        self.camera.resize_frame_shape(0)

        self.array = []

        for i in range(self.count):
            circle = Circle(color=None) \
                .set_fill(hsl2hex((i / self.count, 1, 0.5)), 1) \
                .shift(LEFT * ((self.count - 1) / 2) * 3) \
                .shift(RIGHT * i * 3)

            self.array.append(circle)

        self.play(AnimationGroup(*[FadeIn(circle)
                  for circle in self.array], lag_ratio=0.05))

    def swap(self, a: int, b: int):
        self.play(Swap(self.array[a], self.array[b], path_arc=120 * DEGREES))

        self.array[a], self.array[b] = self.array[b], self.array[a]

    def shuffle(self):
        for b in range(self.count - 1, 0, -1):
            a = random.randrange(0, b)
            self.swap(a, b)

    def destroy_circles(self):
        self.play(AnimationGroup(*[FadeOut(circle)
                  for circle in self.array], lag_ratio=0.05))
        self.array = []
