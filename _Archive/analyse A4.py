#!/usr/bin/env python3

import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

p = 49
samplerate, y = wavfile.read('inharmonicite/sons/49 - A4.wav')
y = y[:, 0]

yf = np.absolute(np.fft.fft(y))
xf = np.arange(yf.size) * 1.0 / yf.size * samplerate

yf = yf[:int(yf.size/2)]
xf = xf[:int(xf.size/2)]

zoom = 0.6
f = 440 * (2 ** ((p - 49) / 12))

harmonics = np.zeros(0)
amplitudes = np.zeros(0)

n_harmonics = 45

for n in range(0, n_harmonics):
  if n == 0:
    center_f = f
  else:
    center_f = harmonics[harmonics.size - 1] / n * (n + 1)

  center = center_f * (xf.size / (samplerate / 2))
  delta = zoom * f * (xf.size / (samplerate / 2))

  xf_zoom = xf[int(center - delta):int(center + delta)]
  yf_zoom = yf[int(center - delta):int(center + delta)]

  harmonics = np.append(harmonics, [round(xf_zoom[np.argmax(yf_zoom)], 2)])
  amplitudes = np.append(amplitudes, [round(yf_zoom[np.argmax(yf_zoom)], 2)])

to_delete = [12, 27, 30, 40, 43]
harmonics = np.delete(harmonics, to_delete)
amplitudes = np.delete(amplitudes, to_delete)

inharmonicity = np.zeros(len(harmonics))
for n in range(0, len(harmonics)):
  inharmonicity[n] = round(1200 * math.log2(harmonics[n] / ((n + 1) * harmonics[0])), 2)

print("{}{}{}{}{}".format("n".rjust(4), "f0".rjust(10), "f".rjust(12), "A".rjust(15), "I".rjust(10)))
for n in range(0, len(harmonics)):
  print("{}{}{}{}{}".format(
    str(n + 1).rjust(4), 
    str((n + 1) * f).replace(".", ",").rjust(10),
    str(harmonics[n]).replace(".", ",").rjust(12),
    str(amplitudes[n]).replace(".", ",").rjust(15),
    str(inharmonicity[n]).replace(".", ",").rjust(10))
  )

# plt.plot(xf_zoom, yf_zoom)
# plt.show()
