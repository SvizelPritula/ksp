from collections import deque


def pop_smallest(a, b):
    if len(a) == 0 and len(b) == 0:
        raise IndexError()
    elif len(b) == 0:
        return a.popleft()
    elif len(a) == 0:
        return b.popleft()
    elif a[0] < b[0]:
        return a.popleft()
    else:
        return b.popleft()


def get_composite_numbers(m, primes):
    input_queue = deque([1])
    yield 1

    for prime in primes:
        feedback_queue = deque()
        result = deque()

        while len(input_queue) > 0 or len(feedback_queue) > 0:
            q = pop_smallest(input_queue, feedback_queue)

            if q * prime > m:
                break

            result.append(q)
            feedback_queue.append(q * prime)
            yield q * prime

        input_queue = result


def get_prime_factors(n):
    table = [set() for _ in range(n + 1)]

    for i in range(2, n+1):
        if len(table[i]) == 0:
            table[i].add(i)

        yield i, table[i]

        for p in table[i]:
            if i + p < len(table):
                table[i + p].add(p)

        table[i] = None


def complement(primes, factors):
    result = []

    for p in primes:
        if p not in factors:
            result.append(p)

    return result


def get_fractions(n):
    yield 0, 1
    yield 1, 1

    primes = []

    for m, factors in get_prime_factors(n):
        if factors == {m}:
            primes.append(m)

        valid_primes = complement(primes, factors)

        for o in get_composite_numbers(m, valid_primes):
            yield o, m
