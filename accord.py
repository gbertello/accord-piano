#!/usr/bin/env python3

import sys
try:
  import tkinter
except:
  print("Tkinter needs to be installed on the system")
  print("brew install python-tk")
  sys.exit(0)

from animation import *
from cache import *
from figure import *
from pitches import *
from stream import *
from window import *


class App(Tk):
  def __init__(self):
    self.pitches = Pitches()
    self.cache = Cache()
    self.stream = Stream(self.cache.get("duration"), self.cache.get("samplerate"), self.cache.get("device"), self.cache.get("channels"))
    self.figure = Figure(self.pitches, self.cache, self.stream)
    self.window = Window(self.pitches, self.cache, self.stream, self.figure)
    self.ani = Animation(self.cache, self.figure) # Need the figure to be declared in window canvas before starting animation
    self.window.mainloop()


if __name__ == "__main__":
  App()
