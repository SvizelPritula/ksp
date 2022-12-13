from random import Random

import math
import numpy

rows = 8
iterations = 128

pairs = []

target = []
for i in range(rows + 1):
    target.append(math.comb(rows, i))

for seed in range(10000):
    random = Random(seed)
    counts = [0] * (rows + 1)

    for i in range(iterations):
        pos = 0

        for r in range(rows):
            pos += random.randrange(2)

        counts[pos] += 1

    dev = numpy.std(numpy.divide(counts, target))
    pairs.append((dev, seed))

print(max(pairs, key=lambda p: p[0]))
