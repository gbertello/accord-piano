#!/usr/bin/env python3
import json
import math

with open("cache.json") as f:
  cache = json.loads(f.read())

harmonics = cache["harmonics"]

i = 33
for j in range(0, 6):
  line = ""
  for i in range(33, 50):
    line += str(harmonics[str(i)][j]).replace(".", ",") + "\t"
  print(line)