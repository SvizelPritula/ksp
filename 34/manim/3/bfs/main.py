from manim import *
from math import sqrt
import networkx as nx
import collections

nodes = list(range(16))
edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (2, 4),
    (3, 4),
    (4, 5),
    (1, 6),
    (6, 7),
    (7, 8),
    (7, 9),
    (8, 9),
    (8, 10),
    (9, 10),
    (6, 11),
    (11, 12),
    (11, 13),
    (13, 14),
    (14, 15),
    (10, 14)
]


class BreadthFirstSearch(Scene):
    def construct(self):
        graph = nx.Graph()
        graph.add_nodes_from(nodes)
        graph.add_edges_from(edges)

        obj = Graph.from_networkx(graph, layout_config={"seed": 0})
        obj.scale(3)

        self.play(Write(obj), run_time=2)

        first_node = 0

        self.play(
            Flash(obj[first_node], color=RED, flash_radius=.3),
            obj[first_node].animate.set_color(RED)
        )

        visited_nodes = {first_node}
        queue = collections.deque([first_node])

        while len(queue) > 0:
            node = queue.popleft()

            self.play(Indicate(obj[node], color=RED))

            for neighbor in graph.neighbors(node):
                if neighbor in visited_nodes:
                    continue

                cursor = Dot(color=RED).scale(2).move_to(obj[node])
                self.add(cursor)
                self.play(cursor.animate.move_to(obj[neighbor]))

                edge = min(node, neighbor), max(node, neighbor)
                self.play(
                    Flash(obj[neighbor], color=RED, flash_radius=.3),
                    obj[neighbor].animate.set_color(RED),
                    obj.edges[edge].animate.set_color(ORANGE)
                )

                self.remove(cursor)

                visited_nodes.add(neighbor)
                queue.append(neighbor)

            self.play(
                obj[node].animate.set_color(ORANGE),
                run_time=0.5
            )
        
        self.play(Unwrite(obj), run_time=2)
