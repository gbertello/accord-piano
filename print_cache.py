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
  print("\t".join([pitch] + values))

