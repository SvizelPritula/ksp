from operations import iter_initial, iter_operations, Expression
from typing import Dict


def can_be_made_by_multiplying(n):
    if n <= 0:
        return False

    for d in range(2, 10):
        while n % d == 0:
            n /= d

    return n == 1


values: Dict[int, Expression] = dict()

for initial in iter_initial():
    values[initial.eval()] = initial

for round in range(8):
    start_points = list(values.keys())

    for value in start_points:
        expr = values[value]

        for op in iter_operations():
            result = op.eval(value)

            if result not in values:
                new_expr = expr.clone()
                new_expr.operations.append(op)
                values[result] = new_expr

for value in sorted(values.keys()):
    if value in values:
        expr = values[value]
        print(f"{value}: {len(expr.operations)} ({expr})")
    else:
        print(f"{value}: Impossible")
