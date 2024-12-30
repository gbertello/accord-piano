#!/usr/bin/env python3

from common import get_stiffness, get_estimated_B
import numpy as np
import matplotlib.pyplot as plt
import math

pitch_min = 36
pitch_max = 77
max_harmonics = 4

# xp = np.zeros(0)
# yp = np.zeros(0)
# for p in range(pitch_min, pitch_max):
#   xp = np.append(xp, p)
#   yp = np.append(yp, get_stiffness(p, pitch_min, max_harmonics))

estimated_B = get_estimated_B(pitch_min, pitch_max, max_harmonics)
xp = np.zeros(0)
yp = np.zeros(0)
for p in range(pitch_min, pitch_max):
  xp = np.append(xp, p)
  yp = np.append(yp, estimated_B[p - pitch_min])

xs = np.zeros(0)
qs = np.zeros(0)
for p in range(pitch_min + 1, pitch_max):
  xs = np.append(xs, p)
  qs = np.append(qs, math.log2((1 + 4 * yp[p - pitch_min]) / (1 + yp[p - pitch_min])) / math.log2((1 + 4 * yp[p - pitch_min - 1]) / (1 + yp[p - pitch_min - 1])))

model = np.polyfit(xs, qs, 0)
estimated_q = np.poly1d(model)(xs)
print(model)

plt.plot(xs, qs, '.', xs, estimated_q, '-')
plt.show()

