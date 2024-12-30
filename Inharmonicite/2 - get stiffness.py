#!/usr/bin/env python3

from common import get_stiffness
import numpy as np

for p in range(1, 89):
  print(str(p).rjust(5) + " " + str(get_stiffness(p, 1, 4)))
