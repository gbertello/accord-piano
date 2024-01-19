import matplotlib.pyplot as plt
import math
import numpy as np
import os
import scipy.io.wavfile as wf

n = 4
freqs_matrix = np.zeros([88, n])
inharms_matrix = np.zeros([88, n])

for p in range(0, 88):
  filename = [f for f in os.listdir('.') if f.startswith(str(p + 1).zfill(2))][0]
  samplerate, data = wf.read(filename)
  signal = data[:, 0]

  yf = np.absolute(np.fft.fft(signal))
  xf = np.arange(yf.size) * samplerate * 1.0 / yf.size

  yf = yf[:int(yf.size/2)]
  xf = xf[:int(xf.size/2)]

  f = 440 * 2 ** (((p + 1) - 49) / 12)

  freqs = np.zeros(n)
  for i in range(0, n):
    fmin = (i + 1) * f * 2 ** (-1 / 12)
    fmax = (i + 1) * f * 2 ** (1 / 12)

    xmin = len(xf[xf < fmin])
    xmax = len(xf[xf < fmax])

    xf_i = xf[xmin:xmax]
    yf_i = yf[xmin:xmax]
    
    freqs[i] = xf[np.argmax(yf_i) + xmin]

  freqs_matrix[p, :] = freqs
  
  inharms = np.zeros(n)
  for i in range(0, n):
    inharms[i] = 1200 * math.log2(freqs[i] / ((i + 1) * freqs[0]))

  inharms_matrix[p, :] = inharms

for p in range(41, 88):
  p_4 = p - 5
  p_5 = p - 7

  freqs = freqs_matrix[p, :]
  freqs_4 = freqs_matrix[p_4, :]
  freqs_5 = freqs_matrix[p_5, :]

  f = 440 * 2 ** ((p + 1 - 49) / 12)
  f_4 = 440 * 2 ** ((p_4 + 1 - 49) / 12)
  f_5 = 440 * 2 ** ((p_5 + 1 - 49) / 12)

  delta_4 = 0
  delta_5 = 0

  while delta_4 + delta_5 <= 0:
    delta_5 = math.log2((f / freqs[0] * freqs[1]) / (f_5 / freqs_5[0] * freqs_5[2])) * 1200
    delta_4 = math.log2((f / freqs[0] * freqs[2]) / (f_4 / freqs_4[0] * freqs_4[3])) * 1200
    f += 0.01

  print(str(p) + "\t" + str(round(440 * 2 ** ((p + 1 - 49) / 12), 2)).replace(".", ",") + "\t" + str(round(f, 2)).replace(".", ","))