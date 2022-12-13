import itertools
from math import floor
from manim import *
import random

random.seed("Benjamin")


class BinarySearch(Scene):
    def construct(self):
        self.count = 30
        self.iterations = 10

        self.initialize_values()
        self.prepare_scene()

        for target in random.sample(self.values, k=self.iterations):
            self.binary_search(target)
            self.reset_search()

        self.tear_down_scene()

    def initialize_values(self):
        self.values = []

        value = 0
        for i in range(self.count):
            value += random.randrange(1, 5)
            self.values.append(value)

    def binary_search(self, target):
        self.display_target(target)

        start = 0
        end = len(self.values) - 1

        while True:
            middle = floor(mid(start, end))
            self.move_arrow_to(middle)

            value = self.values[middle]

            if value < target:
                self.grey_section_out(range(0, middle + 1))
                start = middle + 1
            elif value > target:
                self.grey_section_out(range(middle, len(self.values)))
                end = middle - 1
            else:
                if middle != start or middle != end:
                    self.grey_section_out(itertools.chain(
                        range(0, middle), range(middle + 1, len(self.values))))
                break

    def prepare_scene(self):
        self.shapes = VGroup()
        self.arrow = None

        self.box_spacing = self.camera.frame_width / self.count
        self.box_size = self.box_spacing * 0.8
        self.box_gap = self.box_spacing - self.box_size

        max_text_length = len(str(self.values[-1]))

        self.text_size = self.box_spacing * (0.5 / max_text_length)

        for i in range(self.count):
            shape = VGroup(
                Square(self.box_size),
                Text(str(self.values[i])).scale_to_fit_height(self.text_size)
            )

            self.shapes.add(shape)

        self.shapes.arrange(RIGHT, buff=self.box_gap)
        self.shapes.align_to(DOWN * 3, UP)

        self.play(Write(self.shapes))

    def tear_down_scene(self):
        self.play(Unwrite(self.shapes))

    def display_target(self, target):
        self.target_text = MarkupText(
            f"Target: <b>{target}</b>", font_size=64)
        self.play(Write(self.target_text))

    def move_arrow_to(self, index):
        box = self.shapes[index]

        if self.arrow == None:
            self.arrow = Arrow(UP, DOWN).set_color(RED).next_to(box, UP)

            self.play(Write(self.arrow))
        else:
            self.play(self.arrow.animate.next_to(box, UP))

    def grey_section_out(self, iterator):
        animations = []

        for i in iterator:
            animations.append(self.shapes[i].animate.set_color(DARK_GRAY))

        self.play(*animations)

    def reset_search(self):
        animations = []

        for shape in self.shapes:
            animations.append(shape.animate.set_color(WHITE))

        if self.arrow != None:
            animations.append(Unwrite(self.arrow))
            self.arrow = None

        if self.target_text != None:
            animations.append(Unwrite(self.target_text))
            self.target_text = None

        self.play(*animations)
