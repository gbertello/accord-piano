import matplotlib.pyplot as plt

class Context():
  def __init__(self):
    self.y = []
    self.p = ""
    self.lines = []
    self.vertical_lines = []
    self.axs = []
    self.fig = plt.Figure(figsize = (14, 6))
