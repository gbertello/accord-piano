#!/usr/bin/env python3

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from tkinter import *

from cache import *
from context import *
from pitches import *
from settings import *

class Window(Tk):
  def __init__(self):
    self.pitches = Pitches()
    self.cache = Cache()
    self.fig = plt.Figure(figsize = (14, 6))
    self.context = Context(self.cache, self.pitches, self.fig)

    self.window = Tk()
    self.window.title('Piano tuner')
    self.window.geometry("1500x800")

    self.settings_button = Button(self.window, text ="Settings", command = lambda: self.settings_callback())
    self.settings_button.pack()

    self.previous_pitch_button = Button(self.window, text ="<--", command = lambda: self.previous_pitch_callback())
    self.previous_pitch_button.pack()

    self.pitch_var = StringVar()
    self.pitch_var.set(self.cache.get("pitch"))
    self.pitches_list = OptionMenu(self.window, self.pitch_var, *[v for v in self.pitches.values()], command = lambda e: self.pitch_callback())
    self.pitches_list.pack()

    self.next_pitch_button = Button(self.window, text ="-->", command = lambda: self.next_pitch_callback())
    self.next_pitch_button.pack()

    canvas = FigureCanvasTkAgg(self.fig, master=self.window)
    canvas.get_tk_widget().pack()

    start_button = Button(self.window, text ="Start", command = lambda: self.start_callback())
    start_button.pack()

    stop_button = Button(self.window, text ="Stop", command = lambda: self.stop_callback())
    stop_button.pack()

    save_button = Button(self.window, text ="Save", command = lambda: self.save_callback())
    save_button.pack()

    clear_current_button = Button(self.window, text ="Clear Current", command = lambda: self.clear_current_callback())
    clear_current_button.pack()

    clear_all_button = Button(self.window, text ="Clear All", command = lambda: self.clear_all_callback())
    clear_all_button.pack()

    self.ani = FuncAnimation(self.fig, lambda e: self.context.plot_callback(), interval=self.cache.get("interval"))

    self.window.mainloop()

  def reset(self):
    self.cache.__init__()
    self.fig.clear()
    self.context.__init__(self.cache, self.pitches, self.fig)

  def settings_callback(self):
    self.settings_window = SettingsWindow(self.cache)
    self.settings_window.settings_window.bind("<Destroy>", lambda e: self.settings_destroy_callback(e.widget.winfo_class()))

  def settings_destroy_callback(self, event_type):
    if event_type == "Toplevel":
      self.reset()

  def pitch_callback(self):
    self.cache.__init__()
    self.cache.set("pitch", self.pitch_var.get())
    self.cache.save()
    self.reset()

  def previous_pitch_callback(self):
    self.pitch_var.set(self.pitches.get_previous_pitch(self.cache.get("pitch")))
    self.pitch_callback()

  def next_pitch_callback(self):
    self.pitch_var.set(self.pitches.get_next_pitch(self.cache.get("pitch")))
    self.pitch_callback()

  def start_callback(self):
    self.context.stream.start()

  def stop_callback(self):
    if self.context is not None:
      self.context.stream.stop()

  def save_callback(self):
    self.cache.save()

  def clear_current_callback(self):
    self.cache.delete_harmonic(self.pitch_var.get(), self.pitches)
    self.reset()

  def clear_all_callback(self):
    self.cache.delete_all_harmonics()
    self.reset()


if __name__ == "__main__":
  Window()
