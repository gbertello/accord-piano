#!/usr/bin/env python3

from json import dumps, loads
import os
import numpy as np
import sounddevice as sd
from matplotlib.pyplot import *
from numpy.fft import *

rate = 192000
n_harmonics = 8

def record(start, duration, rate):
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

def display(xf, yf, rate, pure_harmonics, fig, harmonic_frequencies={}, pure_frequencies={}):
  fig.clf()
  for i in range(len(pure_harmonics)):
    subplot(4, 2, i + 1)
    xf_zoom, yf_zoom = get_zoom(xf, yf, rate, pure_harmonics[i])

    for k, v in pure_frequencies:
      if k == i:
        vlines([v], [0], [np.amax(yf_zoom)*1.1], color="orange")

    for k, v in harmonic_frequencies:
      if k == i:
        vlines([v], [0], [np.amax(yf_zoom)*1.1], 'g')

    vlines(xf_zoom, [0], yf_zoom, 'r')
    xlabel('f (Hz)')
    ylabel('A')
    grid()
    axis([xf_zoom[0], xf_zoom[-1], 0, np.amax(yf_zoom)*1.1])

def save_cache():
  with open('cache.json', 'w') as f:
    f.write(dumps(cache, indent=2))

def load_cache():
  if os.path.exists('cache.json'):
    with open('cache.json') as f:
      cache = loads(f.read())
    if 'harmonics' not in cache.keys():
      cache['harmonics'] = {}
  else:
    cache = {"start": 0, "duration": 5, "harmonics": {}}
  return cache

def initialize_parameters(cache):
  start = 0
  if 'start' in cache.keys():
    start = cache['start']

  duration = 5
  if 'duration' in cache.keys():
    duration = cache['duration']

  last_action = "t49"
  if 'last_action' in cache.keys():
    last_action = cache['last_action']

  return start, duration, last_action

def read_key(key):
  if len(key) == 1 or not key[1:].isdigit() or int(key[1:]) < 1 or int(key[1:]) > 88:
    return None
  return int(key[1:])

def get_pure_frequencies(pure_harmonics):
  pure_frequencies = []
  for i in range(0, len(pure_harmonics)):
    pure_frequencies.append((i, pure_harmonics[i]))
  return pure_frequencies

def get_harmonic_frequencies(cache):
  harmonic_frequencies = []
  if str(t + 7) in cache['harmonics'].keys():
    harmonic_frequencies.append((2, cache['harmonics'][str(t + 7)][1])) #qn+
  if str(t - 7) in cache['harmonics'].keys():
    harmonic_frequencies.append((1, cache['harmonics'][str(t - 7)][2])) #qn-
  if str(t + 5) in cache['harmonics'].keys():
    harmonic_frequencies.append((3, cache['harmonics'][str(t + 5)][2])) #qr+
  if str(t - 5) in cache['harmonics'].keys():
    harmonic_frequencies.append((2, cache['harmonics'][str(t - 5)][3])) #qr-
  # if str(t + 4) in cache['harmonics'].keys():
  #   harmonic_frequencies.append((4, cache['harmonics'][str(t + 4)][3])) #t+
  # if str(t - 4) in cache['harmonics'].keys():
  #   harmonic_frequencies.append((3, cache['harmonics'][str(t - 4)][4])) #t-
  # if str(t + 3) in cache['harmonics'].keys():
  #   harmonic_frequencies.append((5, cache['harmonics'][str(t + 3)][4])) #tm+
  # if str(t - 3) in cache['harmonics'].keys():
  #   harmonic_frequencies.append((4, cache['harmonics'][str(t - 3)][5])) #tm-
  # if str(t + 9) in cache['harmonics'].keys():
  #   harmonic_frequencies.append((4, cache['harmonics'][str(t + 9)][2])) #s+
  # if str(t - 9) in cache['harmonics'].keys():
  #   harmonic_frequencies.append((2, cache['harmonics'][str(t - 9)][4])) #s-
  return harmonic_frequencies

def check(cache, t):
  ok = True
  if str(t + 7) in cache["harmonics"].keys() and cache["harmonics"][str(t)][2] <= cache["harmonics"][str(t + 7)][1]:
    print("\033[91m" + "%s (%s) too low for %s" % (t, pitches[t], pitches[t + 7]) + "\033[0m")
    ok = False
  if str(t + 5) in cache["harmonics"].keys() and cache["harmonics"][str(t)][3] >= cache["harmonics"][str(t + 5)][2]:
    print("\033[91m" + "%s (%s) too high for %s" % (t, pitches[t], pitches[t + 5]) + "\033[0m")
    ok = False
  if str(t - 7) in cache["harmonics"].keys() and cache["harmonics"][str(t)][1] >= cache["harmonics"][str(t - 7)][2]:
    print("\033[91m" + "%s (%s) too high for %s" % (t, pitches[t], pitches[t - 7]) + "\033[0m")
    ok = False
  if str(t - 5) in cache["harmonics"].keys() and cache["harmonics"][str(t)][2] <= cache["harmonics"][str(t - 5)][3]:
    print("\033[91m" + "%s (%s) too low for %s" % (t, pitches[t], pitches[t - 5]) + "\033[0m")
    ok = False
  if ok:
    print("\033[92m" + "%s (%s) OK" % (t, pitches[t]) + "\033[0m")
  # if str(t - 4) in cache["harmonics"].keys() and cache["harmonics"][str(t)][3] <= cache["harmonics"][str(t - 4)][4]:
  #   print("\033[91m" + "%s too low for %s" % (pitches[t], pitches[t - 4]) + "\033[0m")
  #   ok = False
  # if str(t - 3) in cache["harmonics"].keys() and cache["harmonics"][str(t)][4] >= cache["harmonics"][str(t - 3)][5]:
  #   print("\033[91m" + "%s too high for %s" % (pitches[t], pitches[t - 3]) + "\033[0m")
  #   ok = False
  # if str(t - 9) in cache["harmonics"].keys() and cache["harmonics"][str(t)][2] <= cache["harmonics"][str(t - 9)][4]:
  #   print("\033[91m" + "%s too low for %s" % (pitches[t], pitches[t - 9]) + "\033[0m")
  #   ok = False
  # if str(t + 4) in cache["harmonics"].keys() and cache["harmonics"][str(t)][4] >= cache["harmonics"][str(t + 4)][3]:
  #   print("\033[91m" + "%s too high for %s" % (pitches[t], pitches[t + 4]) + "\033[0m")
  #   ok = False
  # if str(t + 3) in cache["harmonics"].keys() and cache["harmonics"][str(t)][5] <= cache["harmonics"][str(t + 3)][4]:
  #   print("\033[91m" + "%s too low for %s" % (pitches[t], pitches[t + 3]) + "\033[0m")
  #   ok = False
  # if str(t + 9) in cache["harmonics"].keys() and cache["harmonics"][str(t)][4] >= cache["harmonics"][str(t + 9)][2]:
  #   print("\033[91m" + "%s too high for %s" % (pitches[t], pitches[t + 9]) + "\033[0m")
  #   ok = False

def estimate_pitch(y, rate):
  from scipy.signal import correlate
  corr = correlate(y, y, mode='full')
  corr = corr[len(corr)//2:]

  d = np.diff(corr)
  start = np.nonzero(d > 0)[0][0]

  peak = np.argmax(corr[start:]) + start
  frequency = rate / peak

  key = round((np.log2(frequency / 440) / np.log2(2) * 12) + 49)
  if key not in pitches.keys():
    return None
  else:
    return key


if __name__ == "__main__":
  cache = load_cache()
  start, duration, last_action = initialize_parameters(cache)
  pitches = read_pitches()

  print("Start: %s" % start)
  print("Duration: %s" % duration)
  print("Last action: %s" % last_action)

  fig, ax = subplots(4, 2, figsize=((14,7)))
  ion() # Interactive mode on

  while True:
    print("Action: (t)une / (u)nison / (e)rase cache / s(h)ow cache / (c)heck / (s)tart / (d)uration / (q)uit")
    key = input()
    if key == "":
      key = last_action

    if key.startswith("t"):
      t = read_key(key)
      if t is None:
        print("Set pitch number between 1 and 88")
        continue

      pure_harmonics = get_pure_harmonics(t, n_harmonics)

      print("Tune %s (%s Hz - key %s)" % (pitches[t], pure_harmonics[0], t))
      x, y, xf, yf = record(start, duration, rate)

      harmonics = get_harmonics(xf, yf, rate, pure_harmonics)
      print("Harmonics: %s " % [round(h, 2) for h in harmonics])

      pure_frequencies = get_pure_frequencies(pure_harmonics)
      harmonic_frequencies = get_harmonic_frequencies(cache)
      display(xf, yf, rate, pure_harmonics, fig, harmonic_frequencies, [pure_frequencies[0]])

      cache['harmonics'][str(t)] = harmonics
      check(cache, t)

      show(block=False)
      last_action = key
      cache["last_action"] = last_action
      save_cache()

    elif key.startswith("u"):
      t = read_key(key)
      if t is None:
        print("Set pitch number between 1 and 88")
        continue

      if str(t) not in cache['harmonics'].keys():
        print("Tune pitch first")
        continue

      pure_harmonics = get_pure_harmonics(t, n_harmonics)
      print("Unison %s (%s Hz - key %s)" % (pitches[t], pure_harmonics[0], t))

      x, y, xf, yf = record(start, duration, rate)

      pitch = estimate_pitch(y, rate)
      print("Estimation: %s" % pitch)

      harmonics = get_harmonics(xf, yf, rate, pure_harmonics)
      print("Harmonics: %s " % [round(h, 2) for h in harmonics])

      ref_frequencies = []
      for i in range(0, len(cache['harmonics'][str(t)])):
        ref_frequencies.append((i, cache['harmonics'][str(t)][i]))
      display(xf, yf, rate, pure_harmonics, fig, ref_frequencies)

      print(harmonics)
      show(block=False)
      last_action = key
      cache["last_action"] = last_action
      save_cache()

    elif key.startswith("s"):
      if key == "s":
        print("Start is set to %s" % start)
      elif len(key) == 1 or not key[1:].replace(".", "").isdigit():
        print("Start should be a decimal number")
      else:
        start = float(key[1:])
        cache['start'] = start
        save_cache()
        print("Start set to %s" % start)

    elif key.startswith("d"):
      if key == "d":
        print("Duration is set to %s" % duration)
      elif len(key) == 1 or not key[1:].replace(".", "").isdigit():
        print("Duration should be a decimal number")
      else:
        duration = float(key[1:])
        cache['duration'] = duration
        save_cache()
        print("Duration set to %s" % duration)

    elif key.startswith("h"):
      print("Printing harmonics from cache...")
      for k in sorted([int(i) for i in cache['harmonics'].keys()]):
        print(("%s (%s): " % (k, pitches[k])).ljust(12) + "%s" % cache['harmonics'][str(k)])

    elif key.startswith("c"):
      for t in sorted([int(i) for i in cache['harmonics'].keys()]):
        check(cache, t)

    elif key.startswith("e"):
      t = read_key(key)
      if t is None:
        print("Deleting harmonics from cache...")
        cache['harmonics'] = {}
      else:
        if str(t) in cache['harmonics'].keys():
          del(cache['harmonics'][str(t)])
      save_cache()

    elif key == "q":
      sys.exit(0)
