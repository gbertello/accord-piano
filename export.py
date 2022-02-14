#!/usr/bin/env python3

import json
from cache import load_cache

cache = load_cache()

for k in sorted([int(i) for i in cache["harmonics"].keys()]):
  v = cache["harmonics"][str(k)]
  print(";".join(str(i).replace(".", ",") for i in v))
