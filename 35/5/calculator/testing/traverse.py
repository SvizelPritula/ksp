from operations import iter_initial, iter_operations, Expression
from typing import Dict, Callable, Optional, Iterable, Tuple


def create_initial(restriction: Callable[[Expression, int], bool]) -> Dict[int, Expression]:
    values: Dict[int, Expression] = dict()

    for initial in iter_initial():
        if restriction(initial, -1):
            values[initial.eval()] = initial

    return values


def expand(values: Dict[int, Expression], restriction: Callable[[Expression, int], bool], round: int):
    start_points = list(values.keys())

    for value in start_points:
        expr = values[value]

        for op in iter_operations():
            result = op.eval(value)

            if result not in values or len(values[result].operations) > 1 + len(expr.operations):
                new_expr = expr.clone()
                new_expr.operations.append(op)

                if restriction(new_expr, round):
                    values[result] = new_expr


def find_differences(restriction: Callable[[Expression, int], bool], depth: int, filter: Callable[[int], bool]) -> Iterable[Tuple[int, Expression, Optional[Expression]]]:
    unrestricted = create_initial(lambda _, _r: True)
    for r in range(depth):
        expand(unrestricted, lambda _, _r: True, r)

    restricted = create_initial(restriction)
    for r in range(depth):
        expand(restricted, restriction, r)

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


rounds = 8


def has_small_divisor(value: int):
    for p in [2, 3, 5, 7]:
        if value % p == 0:
            return True

    return False


def is_simple(value: int):
    if value < 2:
        return False

    for p in [2, 3, 5, 7]:
        while value % p == 0:
            value //= p

    return value == 0


def check(ex: Expression, round: int) -> bool:
    val = ex.eval()

    if not has_small_divisor(val):
        return True

    if len(ex.operations) == 0:
        return True

    return ex.operations[-1].operation == '*'


if __name__ == "__main__":
    errors = find_differences(
        check,
        rounds,
        lambda _: True
    )

    errors = sorted(errors, key=lambda t: t[0])

    for (n, unres, res) in errors:
        if res != None:
            print(f"{n}: {unres} / {res}")
        else:
            print(f"{n}: {unres} / Impossible")
