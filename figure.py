import matplotlib.pyplot as plt
from model import *
import numpy as np

class Figure(plt.Figure):
  def __init__(self, pitches, cache, stream):
    self.pitches = pitches
    self.cache = cache
    self.stream = stream
    super().__init__(figsize = (14, 6))
    self.reset()

  def reset(self):
    self.clear()
    self.lines = []
    self.vertical_lines = []
    for n in range(0, self.cache.get("n_harmonics")):
      self.add_subplot((self.cache.get("n_harmonics") - 1) // self.cache.get("fig_width") + 1, self.cache.get("fig_width"), n + 1)
    self.axs = self.axes
    
    self.p = self.pitches.get_pitch_index(self.cache.get("pitch"))
    for n in range(0, self.cache.get("n_harmonics")):
      line, = self.axs[n].plot([], [], lw=1)
      self.lines.append(line)
      self.vertical_lines.append(self.axs[n].axvline(x=0, color="black", lw=0.9))

      f = get_freq(self.p, n + 1)

      self.axs[n].axvline(x=f, color="orange", lw=0.9)

      harmonics = self.cache.get("harmonics")
      if str(self.p) in harmonics and len(harmonics[str(self.p)]) > 0:
        self.print_vertical_line(n, 1, 1, 0, "brown")

      self.print_vertical_line(n, 2, 1, 12, "red")    # Octave
      self.print_vertical_line(n, 3, 2, 7,  "green")  # 5th
      self.print_vertical_line(n, 4, 3, 5,  "purple") # 4th
      self.print_vertical_line(n, 5, 4, 4,  "blue")   # 3rd

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
    yf = np.absolute(np.fft.fft(self.stream.y))
    xf = np.arange(yf.size)*1.0/yf.size*self.cache.get("samplerate")

    yf = yf[:int(yf.size/2)]
    xf = xf[:int(xf.size/2)]

    harmonics = self.cache.get('harmonics')
    harmonics[str(self.p)] = [0] * self.cache.get("n_harmonics")

    pure_frequency = get_pure_frequency(self.p, 1)

    for n in range(0, self.cache.get("n_harmonics")):
      f = get_freq(self.p, n + 1)

      center = f * xf.size / (self.cache.get("samplerate") / 2)
      delta = self.cache.get("zoom") * pure_frequency * xf.size / (self.cache.get("samplerate") / 2)
      
      xf_zoom = xf[int(center - delta):int(center + delta)]
      yf_zoom = yf[int(center - delta):int(center + delta)]
      
      harmonics[str(self.p)][n] = round(xf_zoom[np.argmax(yf_zoom)], 2)

      self.lines[n].set_data(xf_zoom, yf_zoom)
      #self.vertical_lines[n].set_xdata(harmonics[str(self.p)][n])
      
      self.axs[n].set_xlim([(center - delta) * (self.cache.get("samplerate") / 2) / xf.size, (center + delta) * (self.cache.get("samplerate") / 2) / xf.size])
      if len(yf_zoom) > 0:
        self.axs[n].set_ylim([0, max(np.amax(yf_zoom)*1.1, 1)])

    self.cache.set("harmonics", harmonics)

    return self.lines,
