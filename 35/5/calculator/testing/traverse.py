from operations import iter_initial, iter_operations, Expression
from typing import Dict, Callable, Optional, Iterable, Tuple


def create_initial(restriction: Callable[[Expression], bool]) -> Dict[int, Expression]:
    values: Dict[int, Expression] = dict()

    for initial in iter_initial():
        if restriction(initial):
            values[initial.eval()] = initial

    return values


def expand(values: Dict[int, Expression], restriction: Callable[[Expression], bool]):
    start_points = list(values.keys())

    for value in start_points:
        expr = values[value]

        for op in iter_operations():
            result = op.eval(value)

            if result not in values:
                new_expr = expr.clone()
                new_expr.operations.append(op)

                if restriction(new_expr):
                    values[result] = new_expr


def find_differences(restriction: Callable[[Expression], bool], depth: int, filter: Callable[[int], bool]) -> Iterable[Tuple[int, Expression, Optional[Expression]]]:
    unrestricted = create_initial(lambda _: True)
    for _ in range(depth):
        expand(unrestricted, lambda _: True)

    restricted = create_initial(restriction)
    for _ in range(depth):
        expand(restricted, restriction)

    for n in unrestricted.keys():
        if not filter(n):
            continue

        unres = unrestricted[n]

        if n not in restricted:
            yield (n, unres, None)
            continue

        res = restricted[n]

        if len(unres.operations) != len(res.operations):
            yield (n, unres, res)


errors = find_differences(
    lambda e: all((o.operation in ['+'] for o in e.operations)),
    4,
    lambda _: True
)

for (n, unres, res) in errors:
    if res != None:
        print(f"{n}: {unres} / {res}")
    else:
        print(f"{n}: {unres} / Impossible")
