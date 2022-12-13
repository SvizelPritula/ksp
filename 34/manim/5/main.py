import heapq
from manim import *
import networkx as nx
from typing import NamedTuple, Union


class ConnectionEnding(NamedTuple):
    station: int
    time: int


class TimetableEntry(NamedTuple):
    departure: ConnectionEnding
    arrival: ConnectionEnding
    cost: int


class Query(NamedTuple):
    timetable: list[TimetableEntry]
    origin: int
    destination: int


query = Query([
    TimetableEntry(ConnectionEnding(0, 1), ConnectionEnding(2, 2), 650),
    TimetableEntry(ConnectionEnding(0, 2), ConnectionEnding(1, 4), 230),
    TimetableEntry(ConnectionEnding(1, 4), ConnectionEnding(2, 6), 205),
    TimetableEntry(ConnectionEnding(2, 5), ConnectionEnding(3, 7), 245),
    TimetableEntry(ConnectionEnding(2, 7), ConnectionEnding(3, 8), 840),
    TimetableEntry(ConnectionEnding(0, 6), ConnectionEnding(3, 11), 395),
    TimetableEntry(ConnectionEnding(3, 8), ConnectionEnding(4, 9), 415),
    TimetableEntry(ConnectionEnding(3, 2), ConnectionEnding(0, 5), 255),
    TimetableEntry(ConnectionEnding(3, 3), ConnectionEnding(4, 5), 195),
    TimetableEntry(ConnectionEnding(3, 7), ConnectionEnding(5, 9), 615),
    TimetableEntry(ConnectionEnding(4, 9), ConnectionEnding(5, 10), 365),
    TimetableEntry(ConnectionEnding(5, 11), ConnectionEnding(7, 13), 240),
    TimetableEntry(ConnectionEnding(7, 2), ConnectionEnding(0, 5), 270),
    TimetableEntry(ConnectionEnding(7, 6), ConnectionEnding(0, 10), 285),
    TimetableEntry(ConnectionEnding(0, 2), ConnectionEnding(6, 5), 270),
], 0, 7)


class FixedFlash(Flash):
    def __init__(self, point: Union[np.ndarray, Mobject], scene: ThreeDScene, **kwargs) -> None:
        super().__init__(point, **kwargs)
        self.scene = scene

    def begin(self) -> None:
        self.scene.add_fixed_orientation_mobjects(self.lines)
        return super().begin()


class ZIndexThreeDCamera(ThreeDCamera):
    def get_mobjects_to_display(self, *args, **kwargs):
        mobjects = super().get_mobjects_to_display(*args, **kwargs)
        tuples = sorted(enumerate(mobjects),
                        key=lambda p: (p[1].z_index, p[0]))
        return map(lambda p: p[1], tuples)


class ShorterLine3D(Line3D):
    def __init__(self, start=LEFT, end=RIGHT, thickness=0.02, color=None, buffer=0.1, **kwargs):
        self.buffer = buffer
        super().__init__(start, end, thickness, color, **kwargs)

    def set_start_and_end_attrs(self, start, end, **kwargs):
        start_offset = end - start
        start_offset /= np.linalg.norm(start_offset)
        start_offset *= self.buffer

        end_offset = -start_offset

        return super().set_start_and_end_attrs(start + start_offset, end + end_offset, **kwargs)


class CheapestConnectionFinderScene(ThreeDScene):
    def __init__(self, **kwargs):
        super().__init__(ZIndexThreeDCamera, **kwargs)

    def construct(self):
        self.camera.should_apply_shading = False

        timetable = sorted(query.timetable, key=lambda e: e.departure)

        rail_network = nx.Graph(
            (e.departure.station, e.arrival.station) for e in timetable)

        layout = nx.layout.spring_layout(
            rail_network,
            seed=1337,
            center=(0, 0),
            scale=2,
            iterations=100
        )

        def get_position(station: int, height: float = 0):
            pos = layout[station]
            return pos[0] * RIGHT + pos[1] * DOWN + height / 3 * OUT

        table = Table(
            [[
                f"#{e.departure.station}", f"#{e.arrival.station}",
                f"{e.departure.time+6}:00", f"{e.arrival.time+6}:00",
                f"{e.cost} ¥"
            ] for e in timetable],
            col_labels=[Text(str(t)) for t in [
                "From", "To",
                "Departure", "Arrival",
                "Cost"
            ]]
        ).scale(0.3)

        table_title = Text("Timetable", font_size=32)
        table_title.next_to(table, UP)

        self.add_fixed_in_frame_mobjects(table)
        self.play(Write(table), Write(table_title))

        self.wait(1)

        self.play(
            table.animate.scale(0.8).to_corner(UP+RIGHT),
            Unwrite(table_title)
        )

        rail_network_object = VGroup()
        rail_network_nodes: dict[int, VMobject] = dict()
        rail_network_edges: dict[tuple[int], VMobject] = dict()

        for a, b in sorted(rail_network.edges):
            a, b = sorted((a, b))
            obj = Line(get_position(a), get_position(b))

            obj.set_shade_in_3d(True)
            obj.set_z_index(-3)

            rail_network_edges[a, b] = obj
            rail_network_object.add(obj)

        for id in sorted(rail_network.nodes):
            obj = VGroup(
                dot := Dot(radius=0.2),
                text := Text(
                    str(id),
                    color=BLACK,
                    font="sans-serif"
                ).scale_to_fit_height(0.2)
            ).shift(get_position(id))

            obj.set_shade_in_3d(True)

            dot.set_z_index(-2)
            text.set_z_index(-1)

            rail_network_nodes[id] = dot
            rail_network_object.add(obj)

        self.play(FadeIn(rail_network_object))

        self.wait(1)

        self.move_camera(
            phi=75 * DEGREES,
            frame_center=(0, 0, 2),
            run_time=1.5,
            added_anims=[
                self.camera.theta_tracker.animate(
                    rate_func=rate_functions.ease_in_quad).increment_value((0.2 / 2) * 1.5)
            ])
        self.begin_ambient_camera_rotation(rate=0.2)

        self.wait(1)

        station_lines: list[VMobject] = []

        for id in sorted(rail_network.nodes):
            obj = Line3D(
                get_position(id),
                get_position(id, 30),
                thickness=0.02,
                color=WHITE,
                resolution=(8, 8)
            ).set_opacity(0.2)

            obj.set_shade_in_3d(True)
            obj.set_z_index(1)

            station_lines.append(obj)

        self.play(AnimationGroup(
            *(Create(s) for s in station_lines),
            run_time=0.5,
            lag_ratio=0.2
        ))

        self.wait(1)

        node_objects: dict[ConnectionEnding, VMobject] = dict()
        edge_objects: dict[tuple[ConnectionEnding,
                                 ConnectionEnding], VMobject] = dict()

        for index, entry in enumerate(timetable):
            anims: Animation = []

            def make_dot_if_needed(ending: ConnectionEnding):
                if ending not in node_objects:
                    obj = Dot3D(
                        get_position(ending.station, ending.time),
                        radius=0.1,
                        resolution=(8, 8),
                        color=WHITE
                    )

                    anims.append(FadeIn(obj))
                    node_objects[ending] = obj

            make_dot_if_needed(entry.departure)
            make_dot_if_needed(entry.arrival)

            obj = ShorterLine3D(
                get_position(entry.departure.station, entry.departure.time),
                get_position(entry.arrival.station, entry.arrival.time),
                thickness=0.04,
                color=GRAY_A,
                buffer=0.1,
                resolution=(8, 8)
            )

            anims.append(Create(obj))
            edge_objects[entry.departure, entry.arrival] = obj

            self.play(
                AnimationGroup(*anims, lag_ratio=0.3, run_time=0.5),
                Indicate(table.get_rows()[index + 1], color=ORANGE,
                         scale_factor=1, run_time=0.3 * len(anims) + 0.2)
            )

        self.wait(1)
        self.play(Uncreate(table))
        self.wait(1)

        connections = nx.DiGraph(
            (e.departure, e.arrival, {"cost": e.cost}) for e in timetable)

        endpoints_by_station: dict[int, set[ConnectionEnding]] = dict()
        anims: Animation = []

        for id in rail_network.nodes:
            endpoints_by_station[id] = set()

        for entry in timetable:
            endpoints_by_station[entry.departure.station].add(entry.departure)
            endpoints_by_station[entry.arrival.station].add(entry.arrival)

        for id in sorted(rail_network.nodes):
            endpoints = sorted(endpoints_by_station[id], key=lambda e: e.time)

            for i in range(len(endpoints) - 1):
                connections.add_edge(endpoints[i], endpoints[i+1], cost=0)

                obj = ShorterLine3D(
                    get_position(endpoints[i].station, endpoints[i].time),
                    get_position(endpoints[i+1].station, endpoints[i+1].time),
                    thickness=0.04,
                    color=GRAY_A,
                    buffer=0.1,
                    resolution=(8, 8)
                )

                anims.append(Create(obj))
                edge_objects[endpoints[i], endpoints[i+1]] = obj

        self.play(AnimationGroup(*anims, lag_ratio=0.1, run_time=0.5))

        self.play(AnimationGroup(
            *(Uncreate(s) for s in station_lines),
            run_time=0.5,
            lag_ratio=0.2
        ))

        self.wait(5)

        origin = min(endpoints_by_station[query.origin], key=lambda e: e.time)
        destination = max(
            endpoints_by_station[query.destination], key=lambda e: e.time)

        queue: list[tuple[int, ConnectionEnding]] = [(0, origin)]
        connections.nodes[origin]["distance"] = 0

        self.play(
            node_objects[origin].animate.set_color(RED_D),
            FixedFlash(node_objects[origin], self, color=ORANGE)
        )

        while len(queue) > 0:
            _, node = heapq.heappop(queue)

            for neighbour in sorted(connections[node]):
                distance = connections.nodes[node]["distance"]
                distance += connections.edges[node, neighbour]["cost"]

                neighbour_data = connections.nodes[neighbour]

                if "distance" not in neighbour_data or neighbour_data["distance"] > distance:
                    anims: list[Animation] = []

                    if "distance" not in neighbour_data:
                        obj = node_objects[neighbour]
                        anims.append(obj.animate.set_color(RED_D))

                    if "predecesor" in neighbour_data:
                        obj = edge_objects[neighbour_data["predecesor"], neighbour]
                        anims.append(obj.animate.set_color(GRAY_A))

                    obj = edge_objects[node, neighbour]
                    anims.append(obj.animate.set_color(MAROON_D))

                    neighbour_data["distance"] = distance
                    neighbour_data["predecesor"] = node

                    heapq.heappush(queue, (distance, neighbour))

                    self.play(
                        AnimationGroup(*anims, rate_func=0.5),
                        FixedFlash(node_objects[neighbour], self, color=ORANGE)
                    )

        self.wait(3)

        path_nodes: set[ConnectionEnding] = set([destination])
        path_edges: set[tuple[ConnectionEnding, ConnectionEnding]] = set()

        anims: list[Animation] = [
            node_objects[destination].animate(run_time=0.5).set_color(BLUE)
        ]

        network_anims: list[Animation] = [
            rail_network_nodes[destination.station].animate.set_color(BLUE)
        ]

        prev_node = destination

        while prev_node != origin:
            next_node: ConnectionEnding = connections.nodes[prev_node]["predecesor"]

            path_nodes.add(next_node)
            path_edges.add((next_node, prev_node))

            obj = edge_objects[next_node, prev_node]
            anims.append(obj.animate(run_time=0.5).set_color(BLUE_E))

            obj = node_objects[next_node]
            anims.append(obj.animate(run_time=0.5).set_color(BLUE))

            if prev_node.station != next_node.station:
                obj = rail_network_edges[tuple(
                    sorted((next_node.station, prev_node.station)))]
                network_anims.append(obj.animate.set_color(BLUE))

                obj = rail_network_nodes[next_node.station]
                network_anims.append(obj.animate.set_color(BLUE))

            prev_node = next_node

        self.play(Succession(*anims, lag_ratio=0.75))

        first_fade_anims: list[Animation] = []
        second_fade_anims: list[Animation] = []

        for node, obj in sorted(node_objects.items()):
            if node not in path_nodes:
                first_fade_anims.append(FadeOut(obj))
            else:
                second_fade_anims.append(FadeOut(obj))

        for edge, obj in sorted(edge_objects.items()):
            if edge not in path_edges:
                first_fade_anims.append(FadeOut(obj))
            else:
                second_fade_anims.append(FadeOut(obj))

        self.play(*first_fade_anims)

        self.wait(5)

        self.stop_ambient_camera_rotation()
        self.move_camera(
            phi=0,
            theta=round(
                self.camera.theta_tracker.get_value() / (360 * DEGREES) + 0.25
            ) * 360 * DEGREES - 90 * DEGREES,
            frame_center=(0, 0, 0),
            focal_distance=100,
            added_anims=[Succession(
                Wait(0.5),
                AnimationGroup(
                    *(network_anims + second_fade_anims),
                    run_time=0.5
                )
            )]
        )

        self.wait(1)
