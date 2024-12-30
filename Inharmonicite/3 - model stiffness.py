#!/usr/bin/env python3

from common import get_stiffness, get_estimated_B
import matplotlib.pyplot as plt
import numpy as np

pitch_min = 1
pitch_max = 77
max_harmonics = 4

xp = np.zeros(0)
yp = np.zeros(0)
for p in range(pitch_min, pitch_max):
  xp = np.append(xp, p)
  yp = np.append(yp, get_stiffness(p, pitch_min, max_harmonics))
  
plt.plot(xp, yp, '.', xp, get_estimated_B(pitch_min, pitch_max, max_harmonics), '-')
plt.show()
