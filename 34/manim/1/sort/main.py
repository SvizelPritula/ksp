from typing import List
from manim import *
import random

random.seed("Benjamin")


class Sort(Scene):
    def construct(self):
        self.margin = 0.5
        self.count = 30

        self.generate_values()
        self.create_columns()
        self.sort()
        self.remove_columns()

    def generate_values(self):
        self.array: List[float] = []

        step = 1 / (self.count + 1)

        for i in range(self.count):
            value = (i + 1) * step + random.uniform(-step / 3, step / 3)
            self.array.append(value)
        
        random.shuffle(self.array)

    def create_columns(self):
        self.columns: List[Rectangle] = []

        height = self.camera.frame_height - 2 * self.margin
        width = self.camera.frame_width - 2 * self.margin
        width /= self.count * 4 - 1

        for i in range(self.count):
            rect = Rectangle(color=None, width=3 * width, height=self.array[i] * height) \
                .set_fill(WHITE, 1) \
                .shift(RIGHT * (i - ((self.count - 1) / 2)) * 4 * width) \
                .align_to(DOWN * height / 2, DOWN)

            self.columns.append(rect)

        self.play(AnimationGroup(*[GrowFromEdge(rect, DOWN)
                  for rect in self.columns], lag_ratio=0.05))

    def remove_columns(self):
        self.play(AnimationGroup(*[FadeOut(rect)
                  for rect in self.columns], lag_ratio=0.05))

        self.columns = []

    def swap(self, aIndex: int, bIndex: int):
        height = self.camera.frame_height - 2 * self.margin

        self.array[aIndex], self.array[bIndex] = self.array[bIndex], self.array[aIndex]

        a = self.columns[aIndex]
        b = self.columns[bIndex]

        self.play(a.animate.set_fill(YELLOW),
                  b.animate.set_fill(YELLOW), run_time=0.5)

        self.play(
            a.animate.stretch_to_fit_height(
                self.array[aIndex] * height).align_to(DOWN * height / 2, DOWN),
            b.animate.stretch_to_fit_height(
                self.array[bIndex] * height).align_to(DOWN * height / 2, DOWN)
        )

        self.play(a.animate.set_fill(WHITE),
                  b.animate.set_fill(WHITE), run_time=0.5)

    def draw_pivot(self, pivot: int):
        height = self.camera.frame_height - 2 * self.margin
        width = self.camera.frame_width - self.margin

        line = Line(
            LEFT * width / 2 + UP * (pivot - 0.5) * height,
            RIGHT * width / 2 + UP * (pivot - 0.5) * height,
            color=RED
        )

        self.line = line

        self.play(Write(line))

    def remove_pivot(self):
        self.play(Unwrite(self.line))

    def sort(self):
        self.quicksort(0, self.count - 1)

    def quicksort(self, lo: int, hi: int):
        if (hi - lo <= 0):
            return

        pivot = self.array[random.randint(lo, hi)]

        mid = self.partition(lo, hi, pivot)

        self.quicksort(lo, mid)
        self.quicksort(mid + 1, hi)

    def partition(self, lo: int, hi: int, pivot: int):
        first_swap = True
        i, j = lo - 1, hi + 1

        while True:
            ran = False
            while not ran or self.array[i] < pivot:
                i += 1
                ran = True

            ran = False
            while not ran or self.array[j] > pivot:
                j -= 1
                ran = True

            if i >= j:
                if not first_swap:
                    self.remove_pivot()
                return j

            if first_swap:
                self.draw_pivot(pivot)
                first_swap = False

            self.swap(i, j)
