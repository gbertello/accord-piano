#!/usr/bin/env python3

from common import get_harmonics, get_estimated_B
import numpy as np
import math

pitch_min = 1
pitch_max = 77
max_harmonics = 4

estimated_B = get_estimated_B(pitch_min, pitch_max, max_harmonics)

for p in range(pitch_min, pitch_max):
  harmonics = get_harmonics(p, 12)
  
  frequencies = np.zeros(0)
  for k in range(1, len(harmonics) + 1):
    frequency = round(k * math.sqrt(1 + (k ** 2) * estimated_B[p - pitch_min]) / math.sqrt(1 + estimated_B[p - pitch_min]) * harmonics[0], 2)
    frequencies = np.append(frequencies, frequency)

  print(str(p).rjust(5) + "".join([str(h).rjust(10) for h in harmonics]))
  print("".rjust(5) + "".join([str(f).rjust(10) for f in frequencies]))
  print("".rjust(5) + "Estimated B: " + str(estimated_B[p - pitch_min]))
  print("")
