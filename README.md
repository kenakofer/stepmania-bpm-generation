# stepmania-bpm-generation 
A tool to get generate precise stepmania BPMs on less consistent songs by just hitting a key every beat as the song plays. It works well on songs that are basically one tempo, but with small variations.

➡️ ⬅️ ⬆️ ⬇️ 

The first song I used to test (and my first stepmania track ever): Billy Joel's "Piano Man" on youtube. It slides in tempo almost imperceptibly between 172 BPM and 184 BPM. Compared to manually using a metronome to find BPMs, this script was able to get all the BPMs with only a single pass through the audio.

At this point in time, I've only made a single song, so there may likely be a better strategy for tackling this problem. This has been a good exercise nonetheless.

Prerequisites: Python3 with `python-vlc`

Example use:

 - Get audio/video (using youtube-dl for example)
 - Run `record_beat_times.py`, passing in the audio/video file, and the name of the output file.
  ```
  ./record_beat_times.py  Billy\ Joel\ -\ Piano\ Man\ \(Video\)-gxEPV4kolz0.ogg output.times`
  ```
 - As the file plays, hit `Enter` on every beat. Type `q` then `Enter` when you're done
 - The program will write to the output file a list of time diffs between every beat. The next script will smooth out the imprecision in your repeated keyboard hammering.
 - Review the output times file. If you *really* messed up any beats, you'll see a warning. Add or remove rows if you'd like to fix it. Only the first number in each row matters for the next script.
 - Run the BPM generation program. It will smooth out the beat times using a windowed average.
```
./process_beat_times_to_ssc_bpm_pairs.py output.times output.bpms
```
 - Review the output bpms file, which gives beats of the song and the BPM setting at that beat.
 - Copy/paste the output bpms into your `.ssc` and `.sm` files.
 - In stepmania, make sure to reload from the hard drive to see the changes.
