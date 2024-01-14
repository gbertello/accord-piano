#!/usr/bin/env python3
import json
import math

with open("cache 2023-07-25.json") as f:
  cache = json.loads(f.read())

harmonics = cache["harmonics"]

for i in range(1, 89):
  if str(i) in harmonics.keys() and len(harmonics[str(i)]) > 1:
    f1 = harmonics[str(i)][0]
    f2 = harmonics[str(i)][1]
    inharmonicity = (math.log2(f2 / f1) - 1) * 1200
    print(str(i) + "\t" + str(f1).replace(".", ",") + "\t" + str(f2).replace(".", ",") + "\t" + str(inharmonicity).replace(".", ","))
  else:
    print(str(i))