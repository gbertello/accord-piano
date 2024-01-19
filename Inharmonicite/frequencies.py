#!/usr/bin/env python3

import numpy as np

def get_freq(n, k):
  xp = np.arange(1, 89)
  model = [-1.11931577e-09, 3.38888431e-07, -3.02768665e-05, 1.10611651e-03, -1.42900080e-02]
  estimated_B = np.poly1d(model)(xp)

  freqs = np.zeros(0)
  for p in range(1, 89):
    if p < 46:
      freq = 440 * 2 ** ((p - 49) / 12)
    else:
      i = np.where(xp == p - 12)[0]
      freq = (2 * freqs[p - 1 - 12] * np.sqrt((1 + 4 *
              estimated_B[i]) / (1 + estimated_B[i]))).item()
    freqs = np.append(freqs, freq)

  i = np.where(xp == n)[0]
  return round(freqs[n - 1] * k * np.sqrt((1 + (k ** 2) * estimated_B[i]) / (1 + estimated_B[i])).item(), 2)

print(get_freq(49, 3))
