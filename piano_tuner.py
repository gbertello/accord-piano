#!/usr/bin/env python3

from matplotlib.pyplot import *
import numpy as np
from numpy.fft import *
import sounddevice as sd

duration = 5.5
start = 1.5
rate = 44100

last_action = ""

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
  print("Enter action: (p)itch / (f)ourier / (s)how / (z)oom / (d)iapason / (q)uit")
  key = input()
  if key == "":
    key = last_action
 
  if key.lower() in ["p"]:
    x, y, xf, yf = record()
    pitch = xf[np.where(yf == np.amax(yf))[0]]
    print("Pitch: %s" % pitch)
  elif key.lower() in ["f"]:  
    x, y, xf, yf = record()
    figure(figsize=(12,4))
    vlines(xf,[0],yf,'r')
    xlabel('f (Hz)')
    ylabel('A')
    grid()
    axis([0,rate/2,0,1])
    show()
  elif key.lower().startswith("z"):
    x, y, xf, yf = record()
    f = int(key[1:])
    center = int(xf.size/(rate/2)*f)
    delta = int(xf.size/(rate/2)*30)
    xf_zoom = xf[(center - delta):(center + delta)]
    yf_zoom = yf[(center - delta):(center + delta)]
    figure(figsize=(12,4))
    vlines(xf_zoom,[0],yf_zoom,'r')
    xlabel('f (Hz)')
    ylabel('A')
    grid()
    axis([xf_zoom[0],xf_zoom[-1],0,np.amax(yf_zoom)*1.2])
    show()
  elif key.lower() == "s":
    x, y, xf, yf = record()
    max = np.amax(np.absolute(y))
    figure(figsize=(12,4))
    plot(x,y,'r')
    xlabel('t (s)')
    ylabel('A')
    grid()
    axis([0, duration, max*-1.2, max*1.2])
    show()
  elif key.lower() == "d":
    t = np.linspace(0, duration, int(rate * duration))
    sd.play(np.sin(440 * 2 * np.pi * t), rate)
  elif key.lower() == "q":
    sys.exit(0)  

  last_action = key
