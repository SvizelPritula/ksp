from dataclasses import dataclass
from itertools import islice


@dataclass
class FibonacciSquare:
    left: int
    right: int
    top: int
    bottom: int
    number: int
    direction: int


def get_fibonacci_numbers(count=-1):
    a, b = 1, 1
    i = 0

    while count < 0 or i < count:
        yield a
        a, b = b, a + b
        i += 1


def get_fibonacci_squares(count=-1):
    i = 0
    left, right, top, bottom = 0, 1, 0, 1
    direction = 0

    yield FibonacciSquare(left, right, top, bottom, 1, 3)

    for n in islice(get_fibonacci_numbers(count), 1, None):
        if direction == 0:
            left, right, top, bottom = right, right + n, bottom - n, bottom
        elif direction == 1:
            left, right, top, bottom = right - n, right, top - n, top
        elif direction == 2:
            left, right, top, bottom = left - n, left, top, top + n
        elif direction == 3:
            left, right, top, bottom = left, left + n, bottom, bottom + n

        yield FibonacciSquare(left, right, top, bottom, n, direction)

        direction += 1
        direction %= 4

        i += 1
