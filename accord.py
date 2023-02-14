#!/usr/bin/env python3

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
    self.stream = Stream(self.cache)
    self.figure = Figure(self.pitches, self.cache, self.stream)
    self.window = Window(self.pitches, self.cache, self.stream, self.figure)
    self.ani = Animation(self.cache, self.figure) # Need the figure to be declared in window canvas before starting animation
    self.window.mainloop()


if __name__ == "__main__":
  App()
