#!/usr/bin/env python3

import math
import numpy as np
import os
from scipy.io import wavfile

dirname = "inharmonicite/sons/"

xp = np.zeros(0)
yp = np.zeros(0)

for p in range(34, 77):
  xp = np.append(xp, p)

  filename = [name for name in os.listdir(dirname) if name.startswith(str(p).zfill(2))][0]
  samplerate, y = wavfile.read(dirname + filename)
  y = y[:, 0]

  yf = np.absolute(np.fft.fft(y))
  xf = np.arange(yf.size) * 1.0 / yf.size * samplerate

  yf = yf[:int(yf.size/2)]
  xf = xf[:int(xf.size/2)]

  zoom = 0.6
  f = round(440 * (2 ** ((p - 49) / 12)), 2)

  n_harmonics = 4
  harmonics = np.zeros(n_harmonics)
  inharmonicity = np.zeros(n_harmonics)

  for n in range(0, n_harmonics):
    if n == 0:
      center_f = f
    else:
      center_f = harmonics[n - 1] / n * (n + 1)

    center = center_f * (xf.size / (samplerate / 2))
    delta = zoom * f * (xf.size / (samplerate / 2))

    xf_zoom = xf[int(center - delta):int(center + delta)]
    yf_zoom = yf[int(center - delta):int(center + delta)]

    harmonics[n] = round(xf_zoom[np.argmax(yf_zoom)], 2)
    inharmonicity[n] = round(1200 * math.log2(harmonics[n] / ((n + 1) * harmonics[0])), 2)

  coeffs = np.zeros(0)
  for n in range(0, n_harmonics - 1):
    for p in range(n + 1, n_harmonics):
      B = ((n + 1) ** 2 * harmonics[p] ** 2 - (p + 1) ** 2 * harmonics[n] ** 2) / ((p + 1) ** 4 * harmonics[n] ** 2 - (n + 1) ** 4 * harmonics[p] ** 2)
      coeffs = np.append(coeffs, B)

  yp = np.append(yp, np.mean(coeffs))

model = np.polyfit(xp, yp, 4)
estimated_B = np.poly1d(model)(xp)

import matplotlib.pyplot as plt
plt.plot(xp, yp, '.', xp, estimated_B, '-')
plt.show()

freqs = np.zeros(0)
for p in range(1, 89):
  if p < 46:
    freq = 440 * 2 ** ((p - 49) / 12)
  else:
    i = np.where(xp == p - 12)[0]
    freq = (2 * freqs[p - 1 - 12] * np.sqrt((1 + 4 * estimated_B[i]) / (1 + estimated_B[i]))).item()
  freqs = np.append(freqs, freq)

print("{}{}{}".format("p".rjust(5), "f0".rjust(10), "f".rjust(10)))
for p in range(1, 89):
  print("{}{}{}".format(str(p).rjust(5), str(round(440 * 2 ** ((p - 49) / 12), 2)).rjust(10), str(round(freqs[p - 1], 2)).rjust(10)))

print(model)
