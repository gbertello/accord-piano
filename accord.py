#!/usr/bin/env python3

import json
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import sys
from cache import *
from pitches import *
from usage import *
from model import *

device = "Scarlett 4i4 USB, Core Audio"
samplerate = 192000
channels = 1
interval = 30
pitches = load_pitches()
cache = load_cache()

while True:
  usage()
  key = input()

  if key.startswith("c"):
    show_cache(cache)
  elif key.startswith("h"):
    show_cache_harmonics(cache, pitches)
  elif key.startswith("d"):
    store_duration_in_cache(cache, key[1:])
  elif key.startswith("p"):
    store_pitch_in_cache(cache, key[1:], pitches)
  elif key.startswith("z"):
    store_zoom_in_cache(cache, key[1:])
  elif key.startswith("n"):
    store_number_of_harmonics_in_cache(cache, key[1:])
  elif key.startswith("w"):
    store_figure_width_in_cache(cache, key[1:])
  elif key.startswith("i"):
    store_inharmonicity_in_cache(cache, key[1:])
  elif key.startswith("r"):
    store_inharmonicity_ratio_in_cache(cache, key[1:])
  elif key.startswith("e") and len(key) > 1:
    delete_harmonic_in_cache(cache, key[1:], pitches)
  elif key == "e":
    delete_all_harmonics_in_cache(cache)
  elif key == "q":
    sys.exit(0)

  elif key == "":
    # Initialize pitch
    p = get_pitch_index(cache["pitch"], pitches)

    # Initialize frequency
    frequency = 440 * (2 ** ((p - 49) / 12))

    # Initialize signal
    y = np.zeros(int(cache["duration"] * samplerate))

    # Initialize figure
    fig, ax = plt.subplots(cache["n_harmonics"] // cache["fig_width"], cache["fig_width"], figsize=((14,7)), squeeze=False)

    # Get lines for animation
    lines = []
    vertical_lines = []
    for n in range(0, cache["n_harmonics"]):
      i = n // cache["fig_width"]
      j = n % cache["fig_width"]
      line, = ax[i, j].plot([], [], lw=1)
      lines.append(line)
      vertical_lines.append(ax[i, j].axvline(x=0, color="black", lw=0.9))

      pure_frequency = get_pure_frequency(p, n + 1)
      ax[i, j].axvline(x=pure_frequency, color="orange", lw=0.9, linestyle='--')

      corrected_frequency = get_corrected_frequency_2(p, cache["inharmonicity"], cache["inharmonicity_ratio"])
      f = corrected_frequency * (n + 1) * (2 ** ((((n + 1) ** 2 - 1) * cache["inharmonicity"] * (cache["inharmonicity_ratio"] ** (p - 49))) / 1200))
      ax[i, j].axvline(x=f, color="orange", lw=0.9)

      def print_vertical_line(n, p, cache, ax, a, b, interval, color):
        if (n + 1) % a == 0:
          if str(p + interval) in cache["harmonics"].keys():
            m = ((n + 1) // a * b) - 1
            if len(cache["harmonics"][str(p + interval)]) > m:
              ax[i, j].axvline(x=cache["harmonics"][str(p + interval)][m], color=color, lw=0.9)

        if (n + 1) % b == 0:
          if str(p - interval) in cache["harmonics"].keys():
            m = ((n + 1) // b * a) - 1
            if len(cache["harmonics"][str(p - interval)]) > m:
              ax[i, j].axvline(x=cache["harmonics"][str(p - interval)][m], color=color, lw=0.9)

      print_vertical_line(n, p, cache, ax, 2, 1, 12, "red")
      print_vertical_line(n, p, cache, ax, 3, 2, 7,  "green")
      print_vertical_line(n, p, cache, ax, 4, 3, 5,  "purple")
      print_vertical_line(n, p, cache, ax, 5, 4, 4,  "blue")
      print_vertical_line(n, p, cache, ax, 5, 3, 9,  "pink")

    # Define audio callback at this location because it uses global variables
    def audio_callback(indata, frames, time, status):
      global y
      data = indata[:]
      shift = len(data)
      y = np.roll(y, -shift, axis=0)
      y[-shift:] = data.reshape((shift))

    # Define figure callback at this location because it uses global variables
    def plot_callback(frame):
      global y
      yf = np.absolute(np.fft.fft(y))
      xf = np.arange(yf.size)*1.0/yf.size*samplerate

      yf = yf[:int(yf.size/2)]
      xf = xf[:int(xf.size/2)]

      cache["harmonics"][str(p)] = [0] * cache["n_harmonics"]

      for n in range(0, cache["n_harmonics"]):
        i = n // cache["fig_width"]
        j = n % cache["fig_width"]

        corrected_frequency = get_corrected_frequency_2(p, cache["inharmonicity"], cache["inharmonicity_ratio"])
        f = corrected_frequency * (n + 1) * (2 ** ((((n + 1) ** 2 - 1) * cache["inharmonicity"] * (cache["inharmonicity_ratio"] ** (p - 49))) / 1200))

        center = xf.size/(samplerate/2)*f
        delta = cache["zoom"]*center

        xf_zoom = xf[int(center - delta):int(center + delta)]
        yf_zoom = yf[int(center - delta):int(center + delta)]

        cache["harmonics"][str(p)][n] = round(xf_zoom[np.argmax(yf_zoom)], 2)

        lines[n].set_data(xf_zoom, yf_zoom)
        vertical_lines[n].set_xdata(cache["harmonics"][str(p)][n])

        ax[i, j].set_xlim([(center - delta) * (samplerate / 2) / xf.size, (center + delta) * (samplerate / 2) / xf.size])
        if len(yf_zoom) > 0:
          ax[i, j].set_ylim([0, max(np.amax(yf_zoom)*1.1, 1)])

      return lines

    def on_press(event):
      if event.key == ' ':
        global y
        y = np.zeros(int(cache["duration"] * samplerate))

    fig.canvas.mpl_connect('key_press_event', on_press)
    stream = sd.InputStream(device=device, channels=channels, samplerate=samplerate, callback=audio_callback)
    ani = FuncAnimation(fig, plot_callback, interval=interval)

    with stream:
      plt.show()

  elif key.startswith("t"):
    for t in range(37, 50):
      if str(t) in cache["harmonics"].keys():
        ok = True
        if str(t + 7) in cache["harmonics"].keys() and cache["harmonics"][str(t)][2] <= cache["harmonics"][str(t + 7)][1]:
          print("\033[91m" + "%s (%s) too low for %s" % (t, pitches[str(t)], pitches[str(t + 7)]) + "\033[0m")
          ok = False
        if str(t + 5) in cache["harmonics"].keys() and cache["harmonics"][str(t)][3] >= cache["harmonics"][str(t + 5)][2]:
          print("\033[91m" + "%s (%s) too high for %s" % (t, pitches[str(t)], pitches[str(t + 5)]) + "\033[0m")
          ok = False
        if str(t - 7) in cache["harmonics"].keys() and cache["harmonics"][str(t)][1] >= cache["harmonics"][str(t - 7)][2]:
          print("\033[91m" + "%s (%s) too high for %s" % (t, pitches[str(t)], pitches[str(t - 7)]) + "\033[0m")
          ok = False
        if str(t - 5) in cache["harmonics"].keys() and cache["harmonics"][str(t)][2] <= cache["harmonics"][str(t - 5)][3]:
          print("\033[91m" + "%s (%s) too low for %s" % (t, pitches[str(t)], pitches[str(t - 5)]) + "\033[0m")
          ok = False
        if ok:
          print("\033[92m" + "%s (%s) OK" % (t, pitches[str(t)]) + "\033[0m")
      else:
        print("%s not present in cache" % pitches[str(t)])

  with open('cache.json', 'w') as f:
    f.write(json.dumps(cache, indent=2))
