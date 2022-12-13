import numpy
import collections

directions = numpy.array([
    [0, 1],
    [0, -1],
    [1, 0],
    [-1, 0],
])


def read_maze_from_file(path: str) -> tuple[numpy.ndarray, numpy.ndarray]:
    with open(path, 'r', encoding="utf8") as file:
        chars = numpy.array([list(l.strip()) for l in file.readlines()])

        origin = numpy.argwhere(chars == 'x')[0]
        maze = chars != '#'
        return maze, origin


def solve(maze: numpy.ndarray, origin: numpy.ndarray):
    result = numpy.full(maze.shape, -1)
    result[tuple(origin)] = 0

    queue = collections.deque([origin])

    while queue:
        coords = queue.pop()
        distance = result[tuple(coords)] + 1

        for neighbour in directions + coords:
            if maze[tuple(neighbour)] and (result[tuple(neighbour)] > distance or result[tuple(neighbour)] < 0):
                result[tuple(neighbour)] = distance
                queue.append(neighbour)

    return result
