#!/usr/bin/env python3

import math
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.io import wavfile

dirname = "Sons/"

for p in range(1, 89):
  filename = [name for name in os.listdir(dirname) if name.startswith(str(p).zfill(2))][0]

  samplerate, y = wavfile.read(dirname + filename)
  y = y[:, 0]

  yf = np.absolute(np.fft.fft(y))
  xf = np.arange(yf.size) * 1.0 / yf.size * samplerate

  yf = yf[:int(yf.size/2)]
  xf = xf[:int(xf.size/2)]

  zoom = 0.6
  f = round(440 * (2 ** ((p - 49) / 12)), 2)

  n_harmonics = 2
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

  f1 = harmonics[0]
  f2 = harmonics[1]
  inharmonicity = round(1200 * math.log2(f2 / (2 * f1)), 2)
  print("{}{}{}{}".format(
    filename.split(".")[0].rjust(12), 
    str(f1).replace(".", ",").rjust(12),
    str(f2).replace(".", ",").rjust(12),
    str(inharmonicity).replace(".", ",").rjust(12)
  ))

# plt.plot(xf_zoom, yf_zoom)
# plt.show()
