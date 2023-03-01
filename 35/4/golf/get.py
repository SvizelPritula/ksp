#!/usr/bin/env python3

tokens = input().split()
id = tokens[1]

try:
    with open(f"{id}.golf") as file:
        print(file.read())
except FileNotFoundError:
    print("-")
