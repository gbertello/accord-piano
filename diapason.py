#!/usr/bin/env python3

import numpy as np
from scipy.io import wavfile

sampleRate = 44100
frequency = 440
length = 60

t = np.linspace(0, length, sampleRate * length)
y = np.sin(frequency * 2 * np.pi * t)

wavfile.write('diapason.wav', sampleRate, y)
