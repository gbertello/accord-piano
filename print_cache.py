#!/usr/bin/env python3

from cache import *
from pitches import *

cache = load_cache()
pitches = load_pitches()

for p in sorted(cache["harmonics"].keys()):
  print(str(pitches[p]) + "\t" + " ".join([str(x).replace(".", ",") for x in cache["harmonics"][p]]))

