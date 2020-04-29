#!/usr/bin/env python3

from matplotlib.pyplot import *
import numpy as np
from numpy.fft import *
import sounddevice as sd

duration = 5.5
start = 1.5
rate = 44100

last_action = "49"

def record():
  y = sd.rec(int(duration * rate), samplerate=rate, channels=1)
  sd.wait()

  y = y.reshape(y.size,)
  x = np.arange(y.size)/rate

  yf = np.absolute(fft(y[int(rate*start):int(rate*duration)]))
  yf = yf/np.amax(yf)
  xf = np.arange(yf.size)*1.0/yf.size*rate
  
  yf = yf[:int(yf.size/2)]
  xf = xf[:int(xf.size/2)]

  return x, y, xf, yf

while True:
  print("Enter action: note number / (f)ourier / (q)uit")
  key = input()
  if key == "":
    key = last_action
  if key[0] in [str(i) for i in range(10)]:
    x, y, xf, yf = record()
    t = int(key)
    n_harmonics = 8
    harmonics = 440*np.power(2, (t - 49)/12)*np.arange(1, n_harmonics + 1)
    subplots(4, 2, figsize=((14,7)))
    for i in range(n_harmonics):
      if harmonics[i] < rate/2:
        subplot(4, 2, i + 1)
        center = int(xf.size/(rate/2)*harmonics[i])
        delta = int(xf.size/(rate/2)*0.1*harmonics[0])
        xf_zoom = xf[(center - delta):(center + delta)]
        yf_zoom = yf[(center - delta):(center + delta)]
        vlines(xf_zoom,[0],yf_zoom,'r')
        xlabel('f (Hz)')
        ylabel('A')
        grid()
        axis([xf_zoom[0],xf_zoom[-1],0,np.amax(yf_zoom)])
    show()
  elif key.lower() in ["f"]:  
    x, y, xf, yf = record()
    figure(figsize=(12,4))
    vlines(xf,[0],yf,'r')
    xlabel('f (Hz)')
    ylabel('A')
    grid()
    axis([0,rate/2,0,1])
    show()
  elif key.lower() == "q":
    sys.exit(0)  

  last_action = key
