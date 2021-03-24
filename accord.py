#!/usr/bin/env python3

import json
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import os
import sounddevice as sd
import sys
import time

device = 0
samplerate = 192000
channels = 1
interval = 30

with open("pitches.txt", "r") as f:
  pitches = f.read().splitlines()

cache = {}
if os.path.exists("cache.json"):
  with open("cache.json") as f:
    cache = json.loads(f.read())
if "duration" not in cache.keys():
  cache["duration"] = 20
if "zoom" not in cache.keys():
  cache["zoom"] = 0.05
if "pitch" not in cache.keys():
  cache["pitch"] = "LA4"
if "harmonics" not in cache.keys():
  cache["harmonics"] = {}
if "n_harmonics" not in cache.keys():
  cache["n_harmonics"] = 8
if "fig_width" not in cache.keys():
  cache["fig_width"] = 2
if "inharmonicity" not in cache.keys():
  cache["inharmonicity"] = 0
if "inharmonicity_ratio" not in cache.keys():
  cache["inharmonicity_ratio"] = 1
if "inharmonicity_progress_factor" not in cache.keys():
  cache["inharmonicity_progress_factor"] = 1


while True:
  print("""
Action:
  - ()tune
  - (d)uration
  - (p)itch
  - (z)oom
  - (n)umber of harmonics
  - (i)nharmonicity
  - inharmonicity (r)atio
  - inharmonicity progress (f)actor
  - check (t)emper
  - figure (w)idth
  - show (c)ache
  - (e)rase cache
  - (q)uit
""")

  key = input()

  if key.startswith("d"):
    if len(key) <= 1 or not key[1:].replace(".", "").isdigit():
      print("duration should be a decimal number")
    else:
      cache['duration'] = float(key[1:])
      print("duration set to %s" % cache["duration"])

  elif key.startswith("p"):
    if len(key) <= 1 or not key[1:] in pitches:
      print("pitch should be a pitch string (e.g. \"LA4\")")
    else:
      cache['pitch'] = key[1:]
      print("pitch set to %s" % cache["pitch"])

  elif key.startswith("z"):
    if len(key) <= 1 or not key[1:].replace(".", "").isdigit():
      print("zoom should be a decimal number")
    else:
      cache['zoom'] = float(key[1:])
      print("zoom set to %s" % cache["zoom"])

  elif key.startswith("n"):
    if len(key) <= 1 or not key[1:].replace(".", "").isdigit():
      print("number of harmonics should be an integer")
    else:
      cache["n_harmonics"] = int(key[1:])
      print("number of harmonics set to %s" % cache["n_harmonics"])

  elif key.startswith("w"):
    if len(key) <= 1 or not key[1:].replace(".", "").isdigit():
      print("figure width should be an integer")
    else:
      cache["fig_width"] = int(key[1:])
      print("figure width set to %s" % cache["fig_width"])

  elif key.startswith("i"):
    if len(key) <= 1 or not key[1:].replace(".", "").isdigit():
      print("inharmonicity should be a number")
    else:
      cache["inharmonicity"] = float(key[1:])
      print("inharmonicity set to %s" % cache["inharmonicity"])

  elif key.startswith("r"):
    if len(key) <= 1 or not key[1:].replace(".", "").isdigit():
      print("inharmonicity ratio should be a number")
    else:
      cache["inharmonicity_ratio"] = float(key[1:])
      print("inharmonicity ratio set to %s" % cache["inharmonicity_ratio"])

  elif key.startswith("f"):
    if len(key) <= 1 or not key[1:].replace(".", "").isdigit():
      print("inharmonicity progress factor width should be a number")
    else:
      cache["inharmonicity_progress_factor"] = float(key[1:])
      print("inharmonicity progress factor set to %s" % cache["inharmonicity_progress_factor"])

  elif key.startswith("t"):
    for t in range(37, 50):
      if str(t) in cache["harmonics"].keys():
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
      else:
        print("%s not present in cache" % pitches[t])

  elif key.startswith("c"):
    print("Duration: %s" % cache["duration"])
    print("Pitch: %s" % cache["pitch"])
    print("Zoom: %s" % cache["zoom"])
    print("Inharmonicity: %s" % cache["inharmonicity"])
    print("Inharmonicity ratio: %s" % cache["inharmonicity_ratio"])
    print("Inharmonicity progress factor: %s" % cache["inharmonicity_progress_factor"])
    print("Harmonics:")
    for pitch in sorted([int(i) for i in cache['harmonics'].keys()]):
      print(("%s (%s): " % (pitch, pitches[pitch])).ljust(12) + "%s" % cache['harmonics'][str(pitch)])

  elif key.startswith("e"):
    if len(key) == 1:
      print("Are you sure? (y/N)")
      confirm = input()
      if confirm.lower() == "y":
        cache["harmonics"] = {}
        print("cache erased")
    else:
      if key[1:] not in pitches:
        print("Specify pitch in letters like LA4")
      else:
        p = pitches.index(key[1:])
        if str(p) in cache['harmonics'].keys():
          del(cache['harmonics'][str(p)])
          print("harmonic %s deleted" % key[1:])

  elif key == "q":
    sys.exit(0)

  else:
    p = pitches.index(cache["pitch"])
    frequency = 440 * (2 ** ((p - 49) / 12))
    y = np.zeros(int(cache["duration"] * samplerate))
    fig, ax = plt.subplots(cache["n_harmonics"] // cache["fig_width"], cache["fig_width"], figsize=((14,7)))

    lines = []
    for n in range(0, cache["n_harmonics"]):
      i = n // cache["fig_width"]
      j = n % cache["fig_width"]
      line, = ax[i, j].plot([], [], lw=1)
      lines.append(line)

      center = frequency*(n + 1)
      delta = cache["zoom"]*center

    def audio_callback(indata, frames, time, status):
      global y
      data = indata[:]
      shift = len(data)
      y = np.roll(y, -shift, axis=0)
      y[-shift:] = data.reshape((shift))

    def plot_callback(frame):
      global y
      yf = np.absolute(np.fft.fft(y))
      xf = np.arange(yf.size)*1.0/yf.size*samplerate

      yf = yf[:int(yf.size/2)]
      xf = xf[:int(xf.size/2)]

      i = 49
      corrected_frequency = 440

      while i > 12:
        corrected_frequency = corrected_frequency / 2 / (1 + cache["inharmonicity_progress_factor"] * (2 ** ((3 * cache["inharmonicity"] * ((cache["inharmonicity_ratio"] ** (i - 12 - 49)) / 1200))) - 1))
        i -= 12
        print(i, corrected_frequency)

      while i < (p - 1) % 12 + 1:
        corrected_frequency = corrected_frequency * 2 ** (1 / 12)
        i += 1
        print(i, corrected_frequency)

      while i < p:
        corrected_frequency = 2 * corrected_frequency * (1 + cache["inharmonicity_progress_factor"] * (2 ** ((3 * cache["inharmonicity"] * ((cache["inharmonicity_ratio"] ** (i - 49)) / 1200))) - 1))
        i += 12
        print(i, corrected_frequency)

      print(corrected_frequency)
      for n in range(0, cache["n_harmonics"]):
        i = n // cache["fig_width"]
        j = n % cache["fig_width"]

        f = corrected_frequency * (n + 1) * (2 ** ((((n + 1) ** 2 - 1) * cache["inharmonicity"] * (cache["inharmonicity_ratio"] ** (p - 49))) / 1200))

        center = xf.size/(samplerate/2)*f
        delta = cache["zoom"]*center

        xf_zoom = xf[int(center - delta):int(center + delta)]
        yf_zoom = yf[int(center - delta):int(center + delta)]

        ax[i, j].axvline(x=f, color="orange", lw=0.9)
        lines[n].set_data(xf_zoom, yf_zoom)
        ax[i, j].set_xlim([f * (1 - cache["zoom"]), f * (1 + cache["zoom"])])
        if len(yf_zoom) > 0:
          ax[i, j].set_ylim([0, max(np.amax(yf_zoom)*1.1, 1)])

        if (n + 1) % 2 == 0:
          if str(p - 7) in cache["harmonics"].keys():
            i = ((n + 1) // 2 * 3) - 1
            if len(cache["harmonics"][str(p - 7)]) > i:
              ax[n // cache["fig_width"], n % cache["fig_width"]].axvline(x=cache["harmonics"][str(p - 7)][i], color="green", lw=0.9)

          if str(p - 12) in cache["harmonics"].keys():
            i = ((n + 1) * 2) - 1
            if len(cache["harmonics"][str(p - 12)]) > i:
              ax[n // cache["fig_width"], n % cache["fig_width"]].axvline(x=cache["harmonics"][str(p - 12)][i], color="red", lw=0.9)

        if (n + 1) % 3 == 0:
          if str(p + 7) in cache["harmonics"].keys():
            i = ((n + 1) // 3 * 2) - 1
            if len(cache["harmonics"][str(p + 7)]) > i:
              ax[n // cache["fig_width"], n % cache["fig_width"]].axvline(x=cache["harmonics"][str(p + 7)][i], color="green", lw=0.9)

          if str(p - 5) in cache["harmonics"].keys():
            i = ((n + 1) // 3 * 4) - 1
            if len(cache["harmonics"][str(p - 5)]) > i:
              ax[n // cache["fig_width"], n % cache["fig_width"]].axvline(x=cache["harmonics"][str(p - 5)][i], color="purple", lw=0.9)

        if (n + 1) % 4 == 0:
          if str(p + 5) in cache["harmonics"].keys():
            i = ((n + 1) // 4 * 3) - 1
            if len(cache["harmonics"][str(p + 5)]) > i:
              ax[n // cache["fig_width"], n % cache["fig_width"]].axvline(x=cache["harmonics"][str(p + 5)][i], color="purple", lw=0.9)

          if str(p + 12) in cache["harmonics"].keys():
            i = ((n + 1) // 2) - 1
            if len(cache["harmonics"][str(p + 12)]) > i:
              ax[n // cache["fig_width"], n % cache["fig_width"]].axvline(x=cache["harmonics"][str(p + 12)][i], color="red", lw=0.9)

      return lines

    stream = sd.InputStream(device=device, channels=channels, samplerate=samplerate, callback=audio_callback)
    ani = FuncAnimation(fig, plot_callback, interval=interval)

    with stream:
      plt.show()

    yf = np.absolute(np.fft.fft(y))
    xf = np.arange(yf.size)*1.0/yf.size*samplerate

    yf = yf[:int(yf.size/2)]
    xf = xf[:int(xf.size/2)]

    harmonics = []
    for n in range(0, cache["n_harmonics"]):
      center = xf.size/(samplerate/2)*frequency*(n + 1)
      delta = cache["zoom"]*center

      xf_zoom = xf[int(center - delta):int(center + delta)]
      yf_zoom = yf[int(center - delta):int(center + delta)]

      harmonics.append(round(xf_zoom[np.argmax(yf_zoom)], 2))

    print(harmonics)
    cache["harmonics"][str(p)] = harmonics

  with open('cache.json', 'w') as f:
    f.write(json.dumps(cache, indent=2))
