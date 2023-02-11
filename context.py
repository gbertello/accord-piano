import sounddevice as sd
import numpy as np
from model import *

class Context():
  def __init__(self, cache, pitches, fig):
    self.cache = cache
    self.pitches = pitches
    self.p = self.pitches.get_pitch_index(self.cache.get("pitch"))
    self.fig = fig
    for n in range(0, self.cache.get("n_harmonics")):
      self.fig.add_subplot(self.cache.get("n_harmonics") // self.cache.get("fig_width"), self.cache.get("fig_width"), n + 1)
    self.axs = self.fig.axes
    self.lines = []
    self.vertical_lines = []
    self.y = np.zeros(int(self.cache.get("duration") * self.cache.get("samplerate")))
    if "stream" in dir(self) is not None and self.stream.active:
      self.stream.stop()
    self.stream = sd.InputStream(device=self.cache.get("device"), channels=self.cache.get("channels"), samplerate=self.cache.get("samplerate"), callback=lambda indata, *args: self.audio_callback(indata))
    self.init_graphs()

  def audio_callback(self, indata):
    data = indata[:]
    shift = len(data)
    self.y = np.roll(self.y, -shift, axis=0)
    self.y[-shift:] = data.reshape((shift))

  def init_graphs(self):
    for n in range(0, self.cache.get("n_harmonics")):
      line, = self.axs[n].plot([], [], lw=1)
      self.lines.append(line)
      self.vertical_lines.append(self.axs[n].axvline(x=0, color="black", lw=0.9))

      pure_frequency = get_pure_frequency(self.p, n + 1)
      corrected_frequency = get_corrected_frequency_2(self.p, self.cache.get("inharmonicity"), self.cache.get("inharmonicity_ratio"))
      f = corrected_frequency * (n + 1) * (2 ** ((((n + 1) ** 2 - 1) * self.cache.get("inharmonicity") * (self.cache.get("inharmonicity_ratio") ** (self.p - 49))) / 1200))

      self.axs[n].axvline(x=pure_frequency, color="orange", lw=0.9, linestyle='--')
      self.axs[n].axvline(x=f, color="orange", lw=0.9)

      harmonics = self.cache.get("harmonics")
      if str(self.p) in harmonics and len(harmonics[str(self.p)]) > 0:
        self.print_vertical_line(n, 1, 1, 0, "brown")

      self.print_vertical_line(n, 2, 1, 12, "red")
      self.print_vertical_line(n, 3, 2, 7,  "green")
      self.print_vertical_line(n, 4, 3, 5,  "purple")
      self.print_vertical_line(n, 5, 4, 4,  "blue")
      self.print_vertical_line(n, 5, 3, 9,  "pink")

  def print_vertical_line(self, n, a, b, interval, color):
    harmonics = self.cache.get('harmonics')
    if (n + 1) % a == 0:
      if str(self.p + interval) in harmonics.keys():
        m = ((n + 1) // a * b) - 1
        if len(harmonics[str(self.p + interval)]) > m:
          self.axs[n].axvline(x=harmonics[str(self.p + interval)][m], color=color, lw=0.9)

    if (n + 1) % b == 0:
      if str(self.p - interval) in harmonics.keys():
        m = ((n + 1) // b * a) - 1
        if len(harmonics[str(self.p - interval)]) > m:
          self.axs[n].axvline(x=harmonics[str(self.p - interval)][m], color=color, lw=0.9)

  def plot_callback(self):
    yf = np.absolute(np.fft.fft(self.y))
    xf = np.arange(yf.size)*1.0/yf.size*self.cache.get("samplerate")

    yf = yf[:int(yf.size/2)]
    xf = xf[:int(xf.size/2)]

    harmonics = self.cache.get('harmonics')
    harmonics[str(self.p)] = [0] * self.cache.get("n_harmonics")

    for n in range(0, self.cache.get("n_harmonics")):
      corrected_frequency = get_corrected_frequency_2(self.p, self.cache.get("inharmonicity"), self.cache.get("inharmonicity_ratio"))
      f = corrected_frequency * (n + 1) * (2 ** ((((n + 1) ** 2 - 1) * self.cache.get("inharmonicity") * (self.cache.get("inharmonicity_ratio") ** (self.p - 49))) / 1200))

      center = xf.size/(self.cache.get("samplerate")/2)*f
      delta = self.cache.get("zoom")*center

      xf_zoom = xf[int(center - delta):int(center + delta)]
      yf_zoom = yf[int(center - delta):int(center + delta)]

      harmonics[str(self.p)][n] = round(xf_zoom[np.argmax(yf_zoom)], 2)

      self.lines[n].set_data(xf_zoom, yf_zoom)
      self.vertical_lines[n].set_xdata(harmonics[str(self.p)][n])

      self.axs[n].set_xlim([(center - delta) * (self.cache.get("samplerate") / 2) / xf.size, (center + delta) * (self.cache.get("samplerate") / 2) / xf.size])
      if len(yf_zoom) > 0:
        self.axs[n].set_ylim([0, max(np.amax(yf_zoom)*1.1, 1)])

    self.cache.set("harmonics", harmonics)

    return self.lines,
