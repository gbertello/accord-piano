import sounddevice as sd
import numpy as np

class Stream(sd.InputStream):
  def __init__(self, duration, init_samplerate, init_device, init_channels):
    self.duration = duration
    self.init_samplerate = init_samplerate
    self.init_device = init_device
    self.init_channels = init_channels
    self.reset()

  def reset(self):
    self.y = np.zeros(int(self.duration * self.init_samplerate))
    if self.active:
      self.close()
    super().__init__(device=self.init_device, channels=self.init_channels, samplerate=self.init_samplerate, callback=lambda indata, *args: self.audio_callback(indata))

  def audio_callback(self, indata):
    data = indata[:]
    shift = len(data)
    self.y = np.roll(self.y, -shift, axis=0)
    self.y[-shift:] = data.reshape((shift))
