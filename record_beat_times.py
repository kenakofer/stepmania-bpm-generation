#!/usr/bin/env python3

import sys
import vlc
from time import time

audio_file_path = sys.argv[1]

time_file_path = sys.argv[2]
with open(time_file_path, 'w') as f:
    f.write("Time since previous keypress, BPM, Is error likely\n")

p = vlc.MediaPlayer(audio_file_path)


p.play()
start_time = time()
times = []
times_between_beats = []



line = ""
while line != "q":
    new_time = time()
    times.append(new_time)

    if len(times) >= 2:
        time_diff = times[-1] - times[-2]
        times_between_beats.append(time_diff)
        print("Time between beats:", time_diff)
        print("In BPM:", 60.0 / time_diff)

    line = input()

# Since the 0-index delta time is always messed up, approximate it
times_between_beats[0] = (times_between_beats[1] + times_between_beats[2] + times_between_beats[3]) / 3

with open(time_file_path, 'a') as f:
    for i, time_diff in enumerate(times_between_beats):
        f.write(str(time_diff)+", ")
        f.write(str(60 / time_diff)+", ")
        if i > 1:
            ratio = times_between_beats[i-1] / times_between_beats[i-2]
            if ratio > 1.5 or ratio < .67:
                f.write("!!!! Error likely !!!! ")
        f.write("\n")
