#!/usr/bin/env python3

import json
import os
import numpy as np
import sounddevice as sd
from matplotlib.pyplot import *
from numpy.fft import *

duration = 10
start = 1.5
rate = 192000
n_harmonics = 8
sd.default.device = 0

ref = []
cache = {}
last_action = "p49"
t = 49
green_lines = []

if os.path.exists('cache.json'):
  with open('cache.json') as infile:
    cache = json.load(infile)

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

def display(xf, yf, rate, pure_harmonics, fig, green_lines):
  fig.clf()
  for i in range(len(pure_harmonics)):
    subplot(4, 2, i + 1)
    xf_zoom, yf_zoom = get_zoom(xf, yf, rate, pure_harmonics[i])

    for k, v in green_lines:
      if k == i:
        vlines([v], [0], [np.amax(yf_zoom)*1.1], 'g')

    vlines(xf_zoom, [0], yf_zoom, 'r')
    xlabel('f (Hz)')
    ylabel('A')
    grid()
    axis([xf_zoom[0], xf_zoom[-1], 0, np.amax(yf_zoom)*1.1])

def save():
  with open('cache.json', 'w') as outfile:
    json.dump(cache, outfile, indent=2)

pitches = read_pitches()
fig, ax = subplots(4, 2, figsize=((14,7)))
ion()
while True:
  print("Enter action: (p)ure / (u) / (o+) / (o-) / (qn+) / (qn-) / (qr+) / (qr-) / (t+) / (t-) / (r)eference / (v)alidate unison / (e)rase cache / (s)tart / (d)uration / (q)uit")
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

    green_lines = []
    green_lines.append((0, pure_harmonics[0]))

    display(xf, yf, rate, pure_harmonics, fig, green_lines)

    print(harmonics)
    cache[str(t)] = harmonics
    ref = harmonics
    show(block=False)
    last_action = key
    save()

  elif key.startswith("u"):
    if ref == []:
      print("Set reference")
      continue

    pure_harmonics = get_pure_harmonics(t, n_harmonics)
    print("Tune %s from %s (%s Hz)" % (pitches[t], pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)

    green_lines = []
    for i in range(n_harmonics):
      green_lines.append((i, ref[i]))

    display(xf, yf, rate, pure_harmonics, fig, green_lines)

    print(harmonics)
    show(block=False)
    last_action = key
    save()

  elif key.startswith("o-"):
    if ref == [] or t < 13:
      print("Set reference")
      continue

    pure_harmonics = get_pure_harmonics(t - 12, n_harmonics)
    print("Tune %s from %s (%s Hz)" % (pitches[t - 12], pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)

    green_lines = []
    green_lines.append((1, ref[0]))

    display(xf, yf, rate, pure_harmonics, fig, green_lines)

    print(harmonics)
    cache[str(t - 12)] = harmonics
    show(block=False)
    last_action = key
    save()

  elif key.startswith("o+"):
    if ref == [] or t > 76:
      print("Set reference")
      continue

    pure_harmonics = get_pure_harmonics(t + 12, n_harmonics)
    print("Tune %s from %s (%s Hz)" % (pitches[t + 12], pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)

    green_lines = []
    green_lines.append((0, ref[1]))

    display(xf, yf, rate, pure_harmonics, fig, green_lines)

    print(harmonics)
    cache[str(t + 12)] = harmonics
    show(block=False)
    last_action = key
    save()

  elif key.startswith("qn-"):
    if ref == [] or t < 8:
      print("Set reference")
      continue

    pure_harmonics = get_pure_harmonics(t - 7, n_harmonics)
    print("Tune %s from %s (%s Hz)" % (pitches[t - 7], pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)

    green_lines = []
    green_lines.append((2, 3/2*np.power(2, -7/12)*ref[1]))

    display(xf, yf, rate, pure_harmonics, fig, green_lines)

    print(harmonics)
    cache[str(t - 7)] = harmonics
    show(block=False)
    last_action = key
    save()

  elif key.startswith("qn+"):
    if ref == [] or t > 81:
      print("Set reference")
      continue

    pure_harmonics = get_pure_harmonics(t + 7, n_harmonics)
    print("Tune %s from %s (%s Hz)" % (pitches[t + 7], pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)

    green_lines = []
    green_lines.append((1, 2/3*np.power(2, 7/12)*ref[2]))

    display(xf, yf, rate, pure_harmonics, fig, green_lines)

    print(harmonics)
    cache[str(t + 7)] = harmonics
    show(block=False)
    last_action = key
    save()

  elif key.startswith("qr-"):
    if ref == [] or t < 6:
      print("Set reference")
      continue

    pure_harmonics = get_pure_harmonics(t - 5, n_harmonics)
    print("Tune %s from %s (%s Hz)" % (pitches[t - 5], pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)

    green_lines = []
    green_lines.append((3, 4/3*np.power(2, -5/12)*ref[2]))

    display(xf, yf, rate, pure_harmonics, fig, green_lines)

    print(harmonics)
    cache[str(t - 5)] = harmonics
    show(block=False)
    last_action = key
    save()

  elif key.startswith("qr+"):
    if ref == [] or t > 83:
      print("Set reference")
      continue

    pure_harmonics = get_pure_harmonics(t + 5, n_harmonics)
    print("Tune %s from %s (%s Hz)" % (pitches[t + 5], pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)

    green_lines = []
    green_lines.append((2, 3/4*np.power(2, 5/12)*ref[3]))

    display(xf, yf, rate, pure_harmonics, fig, green_lines)

    print(harmonics)
    cache[str(t + 5)] = harmonics
    show(block=False)
    last_action = key
    save()

  elif key.startswith("t-"):
    if ref == [] or t < 5:
      print("Set reference")
      continue

    pure_harmonics = get_pure_harmonics(t - 4, n_harmonics)
    print("Tune %s from %s (%s Hz)" % (pitches[t - 4], pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)

    green_lines = []
    green_lines.append((4, 5/4*np.power(2, -4/12)*ref[3]))

    display(xf, yf, rate, pure_harmonics, fig, green_lines)

    print(harmonics)
    cache[str(t - 4)] = harmonics
    show(block=False)
    last_action = key
    save()

  elif key.startswith("t+"):
    if ref == [] or t > 84:
      print("Set reference")
      continue

    pure_harmonics = get_pure_harmonics(t + 4, n_harmonics)
    print("Tune %s from %s (%s Hz)" % (pitches[t + 4], pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)

    green_lines = []
    green_lines.append((3, 4/5*np.power(2, 4/12)*ref[4]))

    display(xf, yf, rate, pure_harmonics, fig, green_lines)

    print(harmonics)
    cache[str(t + 4)] = harmonics
    show(block=False)
    last_action = key
    save()

  elif key.startswith("s-"):
    if ref == [] or t < 10:
      print("Set reference")
      continue

    pure_harmonics = get_pure_harmonics(t - 9, n_harmonics)
    print("Tune %s from %s (%s Hz)" % (pitches[t - 9], pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)

    green_lines = []
    green_lines.append((4, 5/3*np.power(2, -9/12)*ref[2]))

    display(xf, yf, rate, pure_harmonics, fig, green_lines)

    print(harmonics)
    cache[str(t - 9)] = harmonics
    show(block=False)
    last_action = key
    save()

  elif key.startswith("s+"):
    if ref == [] or t > 79:
      print("Set reference")
      continue

    pure_harmonics = get_pure_harmonics(t + 9, n_harmonics)
    print("Tune %s from %s (%s Hz)" % (pitches[t + 9], pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)

    green_lines = []
    green_lines.append((3, 3/5*np.power(2, 9/12)*ref[4]))

    display(xf, yf, rate, pure_harmonics, fig, green_lines)

    print(harmonics)
    cache[str(t + 9)] = harmonics
    show(block=False)
    last_action = key
    save()

  elif key.startswith("t"):
    if len(key) == 1 or not key[1:].isdigit() or int(key[1:]) < 1 or int(key[1:]) > 88:
      print("Set pitch number between 1 and 88")
      continue

    t = int(key[1:])
    pure_harmonics = get_pure_harmonics(t, n_harmonics)
    print("Tune %s (%s Hz)" % (pitches[t], pure_harmonics[0]))

    x, y, xf, yf = record()
    harmonics = get_harmonics(xf, yf, rate, pure_harmonics)

    green_lines = []
    if str(t + 12) in cache.keys():
      green_lines.append((1, cache[str(t + 12)][0])) #o-
    if str(t - 12) in cache.keys():
      green_lines.append((0, cache[str(t - 12)][1])) #o+
    if str(t + 7) in cache.keys():
      green_lines.append((2, 3/2*np.power(2, -7/12)*cache[str(t + 7)][1])) #qn-
    if str(t - 7) in cache.keys():
      green_lines.append((1, 2/3*np.power(2, 7/12)*cache[str(t - 7)][2])) #qn+
    if str(t + 5) in cache.keys():
      green_lines.append((3, 4/3*np.power(2, -5/12)*cache[str(t + 5)][2])) #qr-
    if str(t - 5) in cache.keys():
      green_lines.append((2, 3/4*np.power(2, 5/12)*cache[str(t - 5)][3])) #qr+
    if str(t + 4) in cache.keys():
      green_lines.append((4, 5/4*np.power(2, -4/12)*cache[str(t + 4)][3])) #t-
    if str(t - 4) in cache.keys():
      green_lines.append((3, 4/5*np.power(2, 4/12)*cache[str(t - 4)][4])) #t+
    if str(t + 9) in cache.keys():
      green_lines.append((4, 5/3*np.power(2, -9/12)*cache[str(t + 9)][2])) #s-
    if str(t - 9) in cache.keys():
      green_lines.append((2, 3/5*np.power(2, 9/12)*cache[str(t - 9)][4])) #s+

    display(xf, yf, rate, pure_harmonics, fig, green_lines)

    print(harmonics)
    cache[str(t)] = harmonics
    ref = harmonics
    show(block=False)
    last_action = key
    save()

  elif key.startswith("r"):
    if len(key) == 1 or not key[1:].isdigit() or int(key[1:]) < 1 or int(key[1:]) > 88:
      print("Set pitch number between 1 and 88")
      continue

    t = int(key[1:])
    print("Set reference %s from cache" % (pitches[t]))

    if str(t) in cache.keys():
      ref = cache[str(t)]
      print(ref)
    else:
      print("Not found")
  elif key.startswith("v"):
    print("Validate unison %s" % (pitches[t]))
    cache[str(t)] = harmonics
    save()
  elif key.startswith("s"):
    if key == "s":
      print("Start is set to %s" % start)
    elif len(key) == 1 or not key[1:].replace(".", "").isdigit():
      print("Start should be a decimal number")
    else:
      start = float(key[1:])
      print("Start set to %s" % start)
  elif key.startswith("d"):
    if key == "d":
      print("Duration is set to %s" % duration)
    elif len(key) == 1 or not key[1:].replace(".", "").isdigit():
      print("Duration should be a decimal number")
    else:
      duration = float(key[1:])
      print("Duration set to %s" % duration)
  elif key.startswith("c"):
    print("Printing cache...")
    for k in sorted(cache.keys()):
      print("%s: %s" % (k, cache[k]))
  elif key.startswith("e"):
    if len(key) == 1 or not key[1:].isdigit() or int(key[1:]) < 1 or int(key[1:]) > 88:
      print("Deleting cache...")
      cache = {}
    else:
      t = int(key[1:])
      if str(t) in cache.keys():
        del(cache[str(t)])
    save()

  elif key == "q":
    sys.exit(0)
