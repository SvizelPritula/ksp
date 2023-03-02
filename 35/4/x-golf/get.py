#!/usr/bin/env python3

with open("sort.golf") as file:
    for line in file:
        line = line.split('#')[0]
        line = line.replace(' ', '').strip()
        print(line, end="")
    print()
