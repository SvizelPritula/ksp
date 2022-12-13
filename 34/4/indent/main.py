from enum import Enum
from typing import Iterator


class Statement(Enum):
    OPERATION = 0
    CONTROL = 1


def parse_input() -> Iterator[Statement]:
    count = int(input())

    for i in range(count):
        line = input().strip()

        if line == "":
            continue

        yield Statement.CONTROL if line.endswith(':') else Statement.OPERATION


def count_indentations(program: Iterator[Statement]) -> int:
    counts = [1]
    skip_deintent = False

    for s in program:
        if not skip_deintent:
            c = 0

            for i in range(len(counts)):
                c += counts[i]
                counts[i] = c

        skip_deintent = False

        if s is Statement.CONTROL:
            counts = counts + [0]
            skip_deintent = True

    return sum(counts)


print(count_indentations(parse_input()) % 1000000007)
