from manim import *

from random import Random

rows = 8
iterations = 128
board_scale = 0.5


class FadeOutCarefully(Animation):
    def __init__(self, mobject: VMobject, **kwargs) -> None:
        super().__init__(mobject, remover=True, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        self.mobject.set_fill(opacity=1-alpha)


class GaltonBoard(Scene):
    def construct(self):
        random = Random(1337)
        counts = [0] * (rows + 1)

        galton_peg_group = VGroup()
        galton_pegs = []

        for r in range(rows):
            row = []

            for d in range(r + 1):
                dot = Dot()

                dot.shift(
                    DOWN * r,
                    RIGHT * (d - r / 2 + 0.5)
                )

                galton_peg_group.add(dot)
                row.append(dot)

            galton_pegs.append(row)

        counters = []
        counter_group = VGroup()

        for d in range(rows + 1):
            text = Text("0")

            text.shift(
                DOWN * rows,
                RIGHT * (d - rows / 2 + 0.5)
            )

            counter_group.add(text)
            counters.append(text)

        galton_board = VGroup(galton_peg_group, counter_group)
        galton_board.center().scale(board_scale).shift(RIGHT * 3.5)

        def make_graph(data):
            maximum = max(*data, 1)
            step = maximum // 10 + 1
            top = maximum + (step - maximum % step) % step

            axes = Axes(
                x_range=(-len(data)/2 + 0.5, len(data)/2 - 0.5),
                y_range=[0, top, step],
                x_length=5,
                y_length=5,
                axis_config={
                    "include_numbers": True,
                    "include_tip": False
                }
            )

            axes.center().shift(LEFT * 3.5)

            line = axes.plot_line_graph(
                [x - len(data) / 2 + 0.5 for x in range(len(data))],
                data
            )

            graph = VGroup(axes, line)

            return graph

        graph = make_graph(counts)

        self.play(FadeIn(galton_board, graph))

        for i in range(iterations):
            speed_factor = 1 if i < 4 else 0.1

            ball = Circle(radius=0.2 * board_scale)
            ball.set_stroke(None, width=0)
            ball.set_fill(RED, opacity=1)

            ball.next_to(galton_pegs[0][0], UP, buff=1)

            rate_func = rate_functions.ease_in_sine

            self.play(
                FadeIn(ball, run_time=0.5 * speed_factor),
                ball.animate(run_time=0.5 * speed_factor, rate_func=rate_func).next_to(
                    galton_pegs[0][0], UP, buff=0)
            )

            pos = 0

            for r in range(1, rows + 1):
                direction = random.randrange(2)
                pos += direction

                shift = [-1, 1][direction]
                points = [
                    ORIGIN,
                    RIGHT * shift * 0.2,
                    RIGHT * shift * 0.5,
                    RIGHT * shift * 0.5 + DOWN
                ]

                points = (board_scale * p + ball.get_center() for p in points)
                path = CubicBezier(*points)

                animations = [MoveAlongPath(
                    ball, path, run_time=0.5 * speed_factor, rate_func=rate_func)]

                if r == rows:
                    counts[pos] += 1

                    animations.append(FadeOutCarefully(
                        ball, run_time=0.5 * speed_factor, rate_func=rate_functions.ease_in_quad))

                    text = Text(str(counts[pos])).scale(
                        board_scale).move_to(counters[pos])

                    animations.append(
                        FadeOut(counters[pos], run_time=speed_factor))
                    animations.append(FadeIn(text, run_time=speed_factor))

                    counter_group.remove(counters[pos])
                    counters[pos] = text
                    counter_group.add(text)

                    new_graph = make_graph(counts)

                    animations.append(Succession(
                        Wait(0.5 * speed_factor), graph.animate(run_time=speed_factor).become(new_graph)))

                self.play(*animations)

        self.wait(2)

        self.play(FadeOut(galton_board, graph))
