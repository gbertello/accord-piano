#!/usr/bin/env python3

from cache import *
from pitches import *
import math

cache = Cache()
pitches = Pitches()

harmonics = cache.get("harmonics")

for p in sorted([int(x) for x in harmonics.keys()]):
  pitch = str(pitches.get_pitch_value(str(p)))
  values = [str(x) for x in harmonics[str(p)]]
  values2 = values.copy()

  for i in range(0, len(values)):
    values2[i] = str(1200 * math.log2(float(values[i]) / ((i + 1) * float(values[0])))).ljust(20)
  print("\t".join([pitch] + values2))

