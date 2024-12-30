#!/usr/bin/env python3

from common import get_pure_frequency, get_estimated_frequency
import numpy as np
import math

pitch_min = 36
pitch_max = 77
max_harmonics = 4
A4 = 442

I = 0.64942526
q = 1.09880929

for p in range(1, 89):
  frequency = get_estimated_frequency(p, I, q, A4)
  print(str(p).rjust(5) + str(round(get_pure_frequency(p, A4), 2)).rjust(10) + str(round(frequency, 2)).rjust(10))
