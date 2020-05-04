#!/usr/bin/env python3

import numpy as np
import sounddevice as sd
from matplotlib.pyplot import *
from numpy.fft import *

duration = 10
start = 1.5
rate = 192000
n_harmonics = 8

ref = []
cache = {}
last_action = "p49"

def record():
  y = sd.rec(int((start+duration) * rate), samplerate=rate, channels=1)
  sd.wait()

  y = y.reshape(y.size,)
  x = np.arange(y.size)/rate

  yf = np.absolute(fft(y[int(rate*start):int(rate*(start+duration))]))
  xf = np.arange(yf.size)*1.0/yf.size*rate
  
  yf = yf[:int(yf.size/2)]
  xf = xf[:int(xf.size/2)]

  return x, y, xf, yf

def get_pure_harmonics(t, n_harmonics):
  pure_harmonics = 440*np.power(2, (t - 49)/12)*np.arange(1, n_harmonics + 1)
  return [round(i, 2) for i in pure_harmonics]

def get_zoom(xf, yf, rate, f):
  center = int(xf.size/(rate/2)*f)
  delta = int(0.05*center)
  xf_zoom = xf[(center - delta):(center + delta)]
  yf_zoom = yf[(center - delta):(center + delta)]
  return xf_zoom, yf_zoom

def get_harmonics(xf, yf, rate, pure_harmonics):
  harmonics = []
  for pure_harmonic in pure_harmonics:
    xf_zoom, yf_zoom = get_zoom(xf, yf, rate, pure_harmonic)
    harmonics.append(round(xf_zoom[np.argmax(yf_zoom)], 2))
  return harmonics

def read_pitches():
  pitches = {}
  i = 1
  for line in open('pitches.txt', 'r').read().splitlines():
    pitches[i] = line
    i += 1
  return pitches

pitches = read_pitches()
while True:
  print("Enter action: (p)ure / (r)eference / (o+) / (o-) / (qn+) / (qn-) / (qr+) / (qr-) / (t+) / (t-) / (f)ourier / (q)uit")
  key = input()
  if key == "":
    key = last_action
  if key.startswith('p'):
    if len(key) == 1 or not key[1:].isdigit() or int(key[1:]) < 1 or int(key[1:]) > 88:
      print("Set pitch number between 1 and 88")
      continue
   
    t = int(key[1:])
    pure_harmonics = get_pure_harmonics(t, n_harmonics) 
    print("Pure %s (%s Hz)" % (pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)
    
    subplots(4, 2, figsize=((14,7)))
    for i in range(n_harmonics):
      subplot(4, 2, i + 1)
      xf_zoom, yf_zoom = get_zoom(xf, yf, rate, pure_harmonics[i])
      
      if i == 0:
        vlines([pure_harmonics[i]], [0], [np.amax(yf_zoom)*1.1], 'g')

      vlines(xf_zoom, [0], yf_zoom, 'r')
      xlabel('f (Hz)')
      ylabel('A')
      grid()
      axis([xf_zoom[0], xf_zoom[-1], 0, np.amax(yf_zoom)*1.1])

    print(harmonics)
    cache[t] = harmonics
    ref = harmonics
    show()
  elif key.startswith("r"):
    if len(key) == 1 or not key[1:].isdigit() or int(key[1:]) < 1 or int(key[1:]) > 88:
      print("Set pitch number between 1 and 88")
      continue

    t = int(key[1:])
    print("Set reference %s from cache" % (pitches[t]))

    if t in cache.keys():
      ref = cache[t]
      print(ref)
    else:
      print("Not found")
  elif key.startswith("o-"):
    if ref == [] or t < 13:
      print("Set reference")
      continue

    pure_harmonics = get_pure_harmonics(t - 12, n_harmonics) 
    print("Tune %s from %s (%s Hz)" % (pitches[t - 12], pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)
        
    subplots(4, 2, figsize=((14,7)))
    for i in range(n_harmonics):
      subplot(4, 2, i + 1)
      xf_zoom, yf_zoom = get_zoom(xf, yf, rate, pure_harmonics[i])
      
      if i == 1:
        vlines([ref[0]], [0], [np.amax(yf_zoom)*1.1], 'g')

      vlines(xf_zoom, [0], yf_zoom, 'r')
      xlabel('f (Hz)')
      ylabel('A')
      grid()
      axis([xf_zoom[0], xf_zoom[-1], 0, np.amax(yf_zoom)*1.1])
    print(harmonics)
    cache[t - 12] = harmonics
    show()
  elif key.startswith("o+"):
    if ref == [] or t > 76:
      print("Set reference")
      continue

    pure_harmonics = get_pure_harmonics(t + 12, n_harmonics) 
    print("Tune %s from %s (%s Hz)" % (pitches[t + 12], pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)
        
    subplots(4, 2, figsize=((14,7)))
    for i in range(n_harmonics):
      subplot(4, 2, i + 1)
      xf_zoom, yf_zoom = get_zoom(xf, yf, rate, pure_harmonics[i])

      if i == 0:
        vlines([ref[1]], [0], [np.amax(yf_zoom)*1.1], 'g')

      vlines(xf_zoom, [0], yf_zoom, 'r')
      xlabel('f (Hz)')
      ylabel('A')
      grid()
      axis([xf_zoom[0], xf_zoom[-1], 0, np.amax(yf_zoom)*1.1])
    print(harmonics)
    cache[t + 12] = harmonics
    show()
  elif key.startswith("qn-"):
    if ref == [] or t < 8:
      print("Set reference")
      continue

    pure_harmonics = get_pure_harmonics(t - 7, n_harmonics) 
    print("Tune %s from %s (%s Hz)" % (pitches[t - 7], pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)
        
    subplots(4, 2, figsize=((14,7)))
    for i in range(n_harmonics):
      subplot(4, 2, i + 1)
      xf_zoom, yf_zoom = get_zoom(xf, yf, rate, pure_harmonics[i])

      if i == 2:
        adjustment_factor = 3/2*np.power(2, -7/12)
        vlines([adjustment_factor*ref[1]], [0], [np.amax(yf_zoom)*1.1], 'g')

      vlines(xf_zoom, [0], yf_zoom, 'r')
      xlabel('f (Hz)')
      ylabel('A')
      grid()
      axis([xf_zoom[0], xf_zoom[-1], 0, np.amax(yf_zoom)*1.1])
    print(harmonics)
    cache[t - 7] = harmonics
    show()
  elif key.startswith("qn+"):
    if ref == [] or t > 81:
      print("Set reference")
      continue

    pure_harmonics = get_pure_harmonics(t + 7, n_harmonics) 
    print("Tune %s from %s (%s Hz)" % (pitches[t + 7], pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)
        
    subplots(4, 2, figsize=((14,7)))
    for i in range(n_harmonics):
      subplot(4, 2, i + 1)
      xf_zoom, yf_zoom = get_zoom(xf, yf, rate, pure_harmonics[i])

      if i == 1:
        adjustment_factor = 2/3*np.power(2, 7/12)
        vlines([adjustment_factor*ref[2]], [0], [np.amax(yf_zoom)*1.1], 'g')

      vlines(xf_zoom, [0], yf_zoom, 'r')
      xlabel('f (Hz)')
      ylabel('A')
      grid()
      axis([xf_zoom[0], xf_zoom[-1], 0, np.amax(yf_zoom)*1.1])
    print(harmonics)
    cache[t + 7] = harmonics
    show()
  elif key.startswith("qr-"):
    if ref == [] or t < 6:
      print("Set reference")
      continue

    pure_harmonics = get_pure_harmonics(t - 5, n_harmonics) 
    print("Tune %s from %s (%s Hz)" % (pitches[t - 5], pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)

    subplots(4, 2, figsize=((14,7)))
    for i in range(n_harmonics):
      subplot(4, 2, i + 1)
      xf_zoom, yf_zoom = get_zoom(xf, yf, rate, pure_harmonics[i])

      if i == 3:
        adjustment_factor = 4/3*np.power(2, -5/12)
        vlines([adjustment_factor*ref[2]], [0], [np.amax(yf_zoom)*1.1], 'g')

      vlines(xf_zoom, [0], yf_zoom, 'r')
      xlabel('f (Hz)')
      ylabel('A')
      grid()
      axis([xf_zoom[0], xf_zoom[-1], 0, np.amax(yf_zoom)*1.1])
    print(harmonics)
    cache[t - 5] = harmonics
    show()
  elif key.startswith("qr+"):
    if ref == [] or t > 83:
      print("Set reference")
      continue

    pure_harmonics = get_pure_harmonics(t + 5, n_harmonics) 
    print("Tune %s from %s (%s Hz)" % (pitches[t + 5], pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)

    subplots(4, 2, figsize=((14,7)))
    for i in range(n_harmonics):
      subplot(4, 2, i + 1)
      xf_zoom, yf_zoom = get_zoom(xf, yf, rate, pure_harmonics[i])

      if i == 2:
        adjustment_factor = 3/4*np.power(2, 5/12)
        vlines([adjustment_factor*ref[3]], [0], [np.amax(yf_zoom)*1.1], 'g')

      vlines(xf_zoom, [0], yf_zoom, 'r')
      xlabel('f (Hz)')
      ylabel('A')
      grid()
      axis([xf_zoom[0], xf_zoom[-1], 0, np.amax(yf_zoom)*1.1])
    print(harmonics)
    cache[t + 5] = harmonics
    show()
  elif key.startswith("t-"):
    if ref == [] or t < 5:
      print("Set reference")
      continue

    pure_harmonics = get_pure_harmonics(t - 4, n_harmonics) 
    print("Tune %s from %s (%s Hz)" % (pitches[t - 4], pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)

    subplots(4, 2, figsize=((14,7)))
    for i in range(n_harmonics):
      subplot(4, 2, i + 1)
      xf_zoom, yf_zoom = get_zoom(xf, yf, rate, pure_harmonics[i])

      if i == 4:
        adjustment_factor = 5/4*np.power(2, -4/12)
        vlines([adjustment_factor*ref[3]], [0], [np.amax(yf_zoom)*1.1], 'g')

      vlines(xf_zoom, [0], yf_zoom, 'r')
      xlabel('f (Hz)')
      ylabel('A')
      grid()
      axis([xf_zoom[0], xf_zoom[-1], 0, np.amax(yf_zoom)*1.1])
    print(harmonics)
    cache[t - 4] = harmonics
    show()
  elif key.startswith("t+"):
    if ref == [] or t > 84:
      print("Set reference")
      continue

    pure_harmonics = get_pure_harmonics(t + 4, n_harmonics) 
    print("Tune %s from %s (%s Hz)" % (pitches[t + 4], pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)

    subplots(4, 2, figsize=((14,7)))
    for i in range(n_harmonics):
      subplot(4, 2, i + 1)
      xf_zoom, yf_zoom = get_zoom(xf, yf, rate, pure_harmonics[i])

      if i == 3:
        adjustment_factor = 4/5*np.power(2, 4/12)
        vlines([adjustment_factor*ref[4]], [0], [np.amax(yf_zoom)*1.1], 'g')

      vlines(xf_zoom, [0], yf_zoom, 'r')
      xlabel('f (Hz)')
      ylabel('A')
      grid()
      axis([xf_zoom[0], xf_zoom[-1], 0, np.amax(yf_zoom)*1.1])
    print(harmonics)
    cache[t + 4] = harmonics
    show()
  elif key.startswith("f"):
    x, y, xf, yf = record()
    figure(figsize=(12,4))
    vlines(xf,[0],yf,'r')
    xlabel('f (Hz)')
    ylabel('A')
    grid()
    axis([0,rate/2,0,1])
    show()
  elif key.startswith("s"):
    if len(key) == 1 or not key[1:].replace(".", "").isdigit():
      print("Start should be a decimal number")
      continue
    start = float(key[1:])
    print("Start set to %s" % start)
  elif key.startswith("d"):
    if len(key) == 1 or not key[1:].replace(".", "").isdigit():
      print("Duration should be a decimal number")
      continue
    duration = float(key[1:])
    print("Duration set to %s" % duration)
  elif key.startswith("q"):
    sys.exit(0)  

  last_action = key
