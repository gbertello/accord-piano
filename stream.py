import sounddevice as sd
import numpy as np

class Stream(sd.InputStream):
  def __init__(self, cache):
    self.cache = cache
    self.reset()

  def reset(self):
    self.y = np.zeros(int(self.cache.get("duration") * self.cache.get("samplerate")))
    if self.active:
      self.close()
    super().__init__(device=self.cache.get("device"), channels=self.cache.get("channels"), samplerate=self.cache.get("samplerate"), callback=lambda indata, *args: self.audio_callback(indata))

  def audio_callback(self, indata):
    data = indata[:]
    shift = len(data)
    self.y = np.roll(self.y, -shift, axis=0)
    self.y[-shift:] = data.reshape((shift))
