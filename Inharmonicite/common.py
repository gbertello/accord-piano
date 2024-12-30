import math
import numpy as np
import os
from scipy.io import wavfile

def get_pure_frequency(p, A4=440):
  return round(A4 * 2 ** ((p - 49) / 12), 2)

def get_nb_harmonics(p, max_harmonics=4):
  return max(min(math.floor(11000 / get_pure_frequency(p)), max_harmonics), 1)

def get_harmonics(p, max_harmonics=4):
  dirname = "Inharmonicite/sons/"
  filename = [name for name in os.listdir(dirname) if name.startswith(str(p).zfill(2))][0]
  samplerate, y = wavfile.read(dirname + filename)
  y = y[:, 0]

  yf = np.absolute(np.fft.fft(y))
  xf = np.arange(yf.size) * 1.0 / yf.size * samplerate

  yf = yf[:int(yf.size/2)]
  xf = xf[:int(xf.size/2)]

  zoom = 0.6
  f = get_pure_frequency(p)

  n_harmonics = get_nb_harmonics(p, max_harmonics)
  harmonics = np.zeros(n_harmonics)

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
  
  return harmonics

def get_stiffness(p, pitch_min=1, max_harmonics=4):
  if p < pitch_min:
    return 0

  harmonics = get_harmonics(p, max_harmonics)
  n_harmonics = len(harmonics)
    
  inharmonicities = np.zeros(0)
  for n in range(0, n_harmonics - 1):
    for p in range(n + 1, n_harmonics):
      inharmonicity = ((n + 1) ** 2 * harmonics[p] ** 2 - (p + 1) ** 2 * harmonics[n] ** 2) / ((p + 1) ** 4 * harmonics[n] ** 2 - (n + 1) ** 4 * harmonics[p] ** 2)
      inharmonicities = np.append(inharmonicities, inharmonicity)
    
  return np.mean(inharmonicity)

def get_model(pitch_min=1, pitch_max=77, max_harmonics=4):
  xp = np.zeros(0)
  yp = np.zeros(0)
  for p in range(pitch_min, pitch_max):
    xp = np.append(xp, p)
    yp = np.append(yp, get_stiffness(p, pitch_min, max_harmonics))

  return np.polyfit(xp, yp, 4)

def get_estimated_B(pitch_min=1, pitch_max=77, max_harmonics=4):
  xp = np.arange(pitch_min, pitch_max)
  model = get_model(pitch_min, pitch_max, max_harmonics)
  return np.poly1d(model)(xp)

def get_estimated_frequency(p, I, q, A4=440):
  return A4 * 2 ** ((p - 49) / 12) * 2 ** (I * (q ** (p - 49) - 1)/ 1200)