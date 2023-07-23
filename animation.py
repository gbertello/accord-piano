from matplotlib.animation import FuncAnimation

class Animation(FuncAnimation):
  def __init__(self, cache, figure):
    self.cache = cache
    self.figure = figure
    super().__init__(self.figure, lambda e: self.figure.plot_callback(), interval=self.cache.get("interval"), cache_frame_data=False)
