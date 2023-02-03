import numpy as np
from pitches import *
from model import *
from cache import *

def init_graphs(context, cache, pitches):
  context.p = get_pitch_index(cache["pitch"], pitches)

  context.fig.clear()
  for n in range(0, cache["n_harmonics"]):
    context.fig.add_subplot(cache["n_harmonics"] // cache["fig_width"], cache["fig_width"], n + 1)

  context.axs = context.fig.axes

  context.lines = []
  context.vertical_lines = []
  for n in range(0, cache["n_harmonics"]):
    line, = context.axs[n].plot([], [], lw=1)
    context.lines.append(line)
    context.vertical_lines.append(context.axs[n].axvline(x=0, color="black", lw=0.9))

    pure_frequency = get_pure_frequency(context.p, n + 1)
    corrected_frequency = get_corrected_frequency_2(context.p, cache["inharmonicity"], cache["inharmonicity_ratio"])
    f = corrected_frequency * (n + 1) * (2 ** ((((n + 1) ** 2 - 1) * cache["inharmonicity"] * (cache["inharmonicity_ratio"] ** (context.p - 49))) / 1200))

    def print_vertical_line(n, p, cache, ax, a, b, interval, color):
      if (n + 1) % a == 0:
        if str(p + interval) in cache["harmonics"].keys():
          m = ((n + 1) // a * b) - 1
          if len(cache["harmonics"][str(p + interval)]) > m:
            context.axs[n].axvline(x=cache["harmonics"][str(p + interval)][m], color=color, lw=0.9)

      if (n + 1) % b == 0:
        if str(p - interval) in cache["harmonics"].keys():
          m = ((n + 1) // b * a) - 1
          if len(cache["harmonics"][str(p - interval)]) > m:
            context.axs[n].axvline(x=cache["harmonics"][str(p - interval)][m], color=color, lw=0.9)

    context.axs[n].axvline(x=pure_frequency, color="orange", lw=0.9, linestyle='--')
    context.axs[n].axvline(x=f, color="orange", lw=0.9)

    if str(context.p) in cache["harmonics"] and len(cache["harmonics"][str(context.p)]) > 0:
      print_vertical_line(n, context.p, cache, context.axs, 1, 1, 0, "brown")

    print_vertical_line(n, context.p, cache, context.axs, 2, 1, 12, "red")
    print_vertical_line(n, context.p, cache, context.axs, 3, 2, 7,  "green")
    print_vertical_line(n, context.p, cache, context.axs, 4, 3, 5,  "purple")
    print_vertical_line(n, context.p, cache, context.axs, 5, 4, 4,  "blue")
    print_vertical_line(n, context.p, cache, context.axs, 5, 3, 9,  "pink")

def plot_callback_function(frame, context, cache):
  yf = np.absolute(np.fft.fft(context.y))
  xf = np.arange(yf.size)*1.0/yf.size*cache["samplerate"]

  yf = yf[:int(yf.size/2)]
  xf = xf[:int(xf.size/2)]

  cache["harmonics"][str(context.p)] = [0] * cache["n_harmonics"]

  for n in range(0, cache["n_harmonics"]):
    corrected_frequency = get_corrected_frequency_2(context.p, cache["inharmonicity"], cache["inharmonicity_ratio"])
    f = corrected_frequency * (n + 1) * (2 ** ((((n + 1) ** 2 - 1) * cache["inharmonicity"] * (cache["inharmonicity_ratio"] ** (context.p - 49))) / 1200))

    center = xf.size/(cache["samplerate"]/2)*f
    delta = cache["zoom"]*center

    xf_zoom = xf[int(center - delta):int(center + delta)]
    yf_zoom = yf[int(center - delta):int(center + delta)]

    cache["harmonics"][str(context.p)][n] = round(xf_zoom[np.argmax(yf_zoom)], 2)

    context.lines[n].set_data(xf_zoom, yf_zoom)
    context.vertical_lines[n].set_xdata(cache["harmonics"][str(context.p)][n])

    context.axs[n].set_xlim([(center - delta) * (cache["samplerate"] / 2) / xf.size, (center + delta) * (cache["samplerate"] / 2) / xf.size])
    if len(yf_zoom) > 0:
      context.axs[n].set_ylim([0, max(np.amax(yf_zoom)*1.1, 1)])

  return context.lines,

def audio_callback_function(indata, context):
  data = indata[:]
  shift = len(data)
  context.y = np.roll(context.y, -shift, axis=0)
  context.y[-shift:] = data.reshape((shift))
