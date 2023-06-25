from operations import iter_initial, iter_operations, Expression
from typing import Dict, Callable, Optional, Iterable, Tuple
from math import log


def create_initial() -> Dict[int, Expression]:
    values: Dict[int, Expression] = dict()

    for initial in iter_initial():
        values[initial.eval()] = initial

    return values


def expand(values: Dict[int, Expression]):
    start_points = list(values.keys())

    for value in start_points:
        expr = values[value]

        for op in iter_operations():
            result = op.eval(value)

            if result not in values or len(values[result].operations) > 1 + len(expr.operations):
                new_expr = expr.clone()
                new_expr.operations.append(op)
                values[result] = new_expr


values = create_initial()
for _ in range(10):
    expand(values)

worst_ratio = 0

for value in sorted(values.keys()):
    if value <= 1000:
        continue

    length = len(values[value].operations)
    ratio = length / log(value, 10)

    worst_ratio = max(ratio, worst_ratio)

print(len(values))
print(worst_ratio)
