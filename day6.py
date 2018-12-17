#!/usr/bin/env python3

import sys
from collections import defaultdict

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

coords = [(int(line.split(', ')[0]), int(line.split(', ')[1])) for line in sys.stdin.readlines()]

# establish bounding box
x_min = min(coords, key=(lambda coord: coord[0]))[0]
x_max = max(coords, key=(lambda coord: coord[0]))[0]
y_min = min(coords, key=(lambda coord: coord[1]))[1]
y_max = max(coords, key=(lambda coord: coord[1]))[1]

# We'll remove coords from the list of candidates if we find that their region is infinite (i.e. borders the bounding box)
candidates = set(coords)
area_sizes = defaultdict(int)

# Strategy 1
for x in range(x_min, x_max + 1):
    for y in range(y_min, y_max + 1):
        distances = [(coord, manhattan_distance((x, y), coord)) for coord in coords]
        distances.sort(key=(lambda x: x[1]))
        if distances[0][1] < distances[1][1]: # the point counts
            closest_point = distances[0][0]
            area_sizes[closest_point] += 1
            if x == x_min or x == x_max or y == y_min or y == y_max: # point's region is infinite
                if closest_point in candidates:
                    candidates.remove(closest_point)

print(max([area_sizes[candidate] for candidate in candidates]))

# Strategy 2
# Bounding box here is not optimal.
region_size = 0
for x in range(x_min - 100, x_max + 100):
    for y in range(y_min - 100, y_max + 100):
        total_distance = sum([manhattan_distance((x, y), coord) for coord in coords])
        if total_distance < 10000:
            region_size += 1

print(region_size)
