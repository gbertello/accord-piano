#!/usr/bin/env python3

from common import get_harmonics

for p in range(1, 89):
  print(str(p).rjust(5) + "".join([str(h).rjust(10) for h in get_harmonics(p, 12)]))
