#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from numpy.fft import fft
import sounddevice as sd
import time

freq = 440*3
duration = 3 #10
rate = 96000
interval = 30

sd.default.channels = 1
sd.default.samplerate = rate
sd.default.blocksize = int(rate/10)

N = int(duration*rate)
x = np.arange(N)/rate
y = np.zeros(N)
xf = np.arange(N)/duration
yf = np.zeros(N)

center = int(N/rate*freq)
delta = int(0.05*center)
xf_zoom = xf[(center - delta):(center + delta)]
yf_zoom = yf[(center - delta):(center + delta)]

def animate(frame):
  #ax.set_ylim(min(y), max(y))
  #line.set_data(x, y)

  #ax.set_ylim(min(yf), max(yf))
  #line.set_data(xf, yf)

  ax.set_ylim(min(yf_zoom), max(yf_zoom))
  line.set_data(xf_zoom, yf_zoom)
  return line,

def callback(indata, frames, time, status):
  global y, yf, yf_zoom, N
  y = np.append(y, indata[:])
  y = y[-N:]
  y = y.reshape(N,)

  yf = np.absolute(fft(y))

  yf_zoom = yf[(center - delta):(center + delta)]

print("Press enter to start")
input()

fig, ax = plt.subplots()
line, = plt.plot([],[])

#plt.axis([0, duration, -1, 1])
#line.set_data(x, y)

#plt.axis([0, 10*freq, 0, 500])
#line.set_data(xf, yf)

plt.axis([xf_zoom[0], xf_zoom[-1], 0, 1.1])
line.set_data(xf_zoom, xf_zoom)

with sd.InputStream(callback=callback):
  myAnimation = FuncAnimation(fig, animate, interval=interval, blit=False)
  plt.show()
