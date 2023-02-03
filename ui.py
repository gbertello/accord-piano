#! /usr/bin/env python3

from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import sounddevice as sd

from cache import *
from callback import *
from pitches import *
from model import *
from settings import *
from context import *

pitches = load_pitches()
cache = load_cache()
context = Context()
stream = sd.InputStream()

def pitch_callback(context, pitches, cache, pitch):
  cache = load_cache()
  cache["pitch"] = pitch
  save_cache(cache)
  init(context, pitches, cache)

def plot_callback(frame, context, cache):
  return plot_callback_function(frame, context, cache)

def audio_callback(indata, context):
  audio_callback_function(indata, context)

def start_callback(context, pitches, cache):
  global stream
  context.y = np.zeros(int(cache["duration"] * cache["samplerate"]))
  if stream is not None and stream.active:
    stream.stop()
  init(context, pitches, cache)
  stream.start()
  stream.in_use = True

def stop_callback():
  global stream
  if stream is not None:
    stream.stop()

def save_callback(cache):
  save_cache(cache)

def settings_destroy_callback(context, pitches, cache, event_type):
  if event_type == "Toplevel":
    cache = load_cache()
    init(context, pitches, cache)

def settings_callback(cache):
  settings_window = SettingsWindow(cache)
  settings_window.settings_window.bind("<Destroy>", lambda e: settings_destroy_callback(context, pitches, cache, e.widget.winfo_class()))

def clear_current_callback(context, pitches, cache, pitch):
  delete_harmonic_in_cache(cache, pitch, pitches)
  init(context, pitches, cache)

def clear_all_callback(context, pitches, cache):
  delete_all_harmonics_in_cache(cache)
  init(context, pitches, cache)

def init(context, pitches, cache):
  global stream

  cache = load_cache()
  cache["pitch"] = pitch_var.get()
  stream = sd.InputStream(device=cache["device"], channels=cache["channels"], samplerate=cache["samplerate"], callback=lambda indata, *args: audio_callback(indata, context))
  context.y = np.zeros(int(cache["duration"] * cache["samplerate"]))
  init_graphs(context, cache, pitches)

window = Tk()
window.title('Piano tuner')
window.geometry("1500x800")

settings_button = Button(window, text ="Settings", command = lambda: settings_callback(cache))
settings_button.pack()

pitch_var = StringVar()
pitch_var.set(cache["pitch"])
pitches_list = OptionMenu(window, pitch_var, *[v for v in pitches.values()], command = lambda e: pitch_callback(context, pitches, cache, pitch_var.get()))
pitches_list.pack()

canvas = FigureCanvasTkAgg(context.fig, master=window)
canvas.get_tk_widget().pack()

start_button = Button(window, text ="Start", command = lambda: start_callback(context, pitches, cache))
start_button.pack()

stop_button = Button(window, text ="Stop", command = stop_callback)
stop_button.pack()

save_button = Button(window, text ="Save", command = lambda: save_callback(cache))
save_button.pack()

clear_current_button = Button(window, text ="Clear Current", command = lambda: clear_current_callback(context, pitches, cache, pitch_var.get()))
clear_current_button.pack()

clear_all_button = Button(window, text ="Clear All", command = lambda: clear_all_callback(context, pitches, cache))
clear_all_button.pack()

devices = [d['name'] for d in sd.query_devices()]
if len(devices) == 0:
  print("No sound device exists")
  exit()

if "device" not in cache or cache["device"] not in devices: cache["device"] = devices[0]

init(context, pitches, cache)
ani = FuncAnimation(context.fig, plot_callback, fargs=(context, cache,), interval=cache["interval"])
window.mainloop()
