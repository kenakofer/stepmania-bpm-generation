#!/usr/bin/env python3

import sys
from time import time


BEATS_BEFORE_STARTING = 15
BEATS_BETWEEN_BPM_MARKINGS = 3
FORMAT="{:.3f}"

CONSTANT_WINDOW_RADIUS = 10
DIMINISHING_WINDOW_RADIUS = 10
TOTAL_WINDOW_RADIUS = CONSTANT_WINDOW_RADIUS + DIMINISHING_WINDOW_RADIUS
TOTAL_WINDOW_WIDTH = TOTAL_WINDOW_RADIUS * 2 + 1
WINDOW_WEIGHTS = \
    [i/DIMINISHING_WINDOW_RADIUS for i in range(DIMINISHING_WINDOW_RADIUS)] + \
    [1.0] * (CONSTANT_WINDOW_RADIUS * 2 + 1) + \
    [i/DIMINISHING_WINDOW_RADIUS for i in range(DIMINISHING_WINDOW_RADIUS, -1, -1)]

def windowed_average(values, index):
    total_weight = 0
    total_value = 0
    for window_i in range(TOTAL_WINDOW_WIDTH):
        value_i = index - TOTAL_WINDOW_RADIUS + window_i
        if value_i < 0 or value_i >= len(values):
            continue
        total_weight += WINDOW_WEIGHTS[window_i]
        total_value += WINDOW_WEIGHTS[window_i] * values[value_i]
    return total_value / total_weight

time_file_path = sys.argv[1]
bpm_file_path = sys.argv[2]
contents = []
times = []
with open(time_file_path, 'r') as f:
    contents = f.readlines()[1:] # Remove header line
    times = [float(line[0:line.index(",")]) for line in contents]

output_string = "#BPMS:"

beat_number = 0
bpm = bpm = 60.0/windowed_average(times, 0)
line = FORMAT.format(0)+"="+FORMAT.format(bpm)+","
output_string += line + "\n"
print(line)
for i, t in enumerate(times):
    beat_number = BEATS_BEFORE_STARTING + i
    if beat_number == 0 or beat_number % BEATS_BETWEEN_BPM_MARKINGS > 0 :
        continue
    bpm = 60.0/windowed_average(times, i)
    line = FORMAT.format(beat_number)+"="+FORMAT.format(bpm)+","
    output_string += line + "\n"
    print(line)

output_string = output_string[:-2] + ";\n" # Replace final comma

with open(bpm_file_path, 'w') as f:
    f.write(output_string)

