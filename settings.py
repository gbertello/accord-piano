from tkinter import *
import sounddevice as sd
from cache import save_cache

class SettingsWindow:
  def __init__(self, cache):
    self.cache = cache

    self.devices = [d['name'] for d in sd.query_devices()]
    if len(self.devices) == 0:
      print("No sound device exists")
      exit()

    if "device" not in self.cache or self.cache["device"] not in self.devices: self.cache["device"] = self.devices[0]
    if self.cache["device"] not in self.devices: self.cache["device"] = self.devices[0]
    if "samplerate" not in self.cache: self.cache["samplerate"] = 192000
    if "channels" not in self.cache: self.cache["channels"] = 1
    if "interval" not in self.cache: self.cache["interval"] = 30
    if "duration" not in self.cache: self.cache["duration"] = 5
    if "zoom" not in self.cache: self.cache["zoom"] = 0.05
    if "n_harmonics" not in self.cache: self.cache["n_harmonics"] = 6
    if "fig_width" not in self.cache: self.cache["fig_width"] = 3
    if "inharmonicity" not in self.cache: self.cache["inharmonicity"] = 0.58
    if "inharmonicity_ratio" not in self.cache: self.cache["inharmonicity_ratio"] = 1.09

    self.settings_window = Toplevel()
    self.settings_window.title('Settings')
    self.settings_window.geometry("300x600")

    self.device_label_var = StringVar()
    self.device_label_var.set("Device: ")
    self.device_label = Label(self.settings_window, textvariable = self.device_label_var)
    self.device_label.pack()

    self.device = StringVar()
    self.device.set(self.cache["device"])
    self.device_list = OptionMenu(self.settings_window, self.device, *self.devices)
    self.device_list.pack()

    self.samplerate_label_var = StringVar()
    self.samplerate_label_var.set("Sample rate: ")
    self.samplerate_label = Label(self.settings_window, textvariable = self.samplerate_label_var)
    self.samplerate_label.pack()

    self.samplerate_entry = Entry(self.settings_window)
    self.samplerate_entry.insert(0, self.cache["samplerate"])
    self.samplerate_entry.pack()

    self.channels_label_var = StringVar()
    self.channels_label_var.set("Channels: ")
    self.channels_label = Label(self.settings_window, textvariable = self.channels_label_var)
    self.channels_label.pack()

    self.channels_entry = Entry(self.settings_window)
    self.channels_entry.insert(0, self.cache["channels"])
    self.channels_entry.pack()

    self.interval_label_var = StringVar()
    self.interval_label_var.set("Interval: ")
    self.interval_label = Label(self.settings_window, textvariable = self.interval_label_var)
    self.interval_label.pack()

    self.interval_entry = Entry(self.settings_window)
    self.interval_entry.insert(0, self.cache["interval"])
    self.interval_entry.pack()

    self.duration_label_var = StringVar()
    self.duration_label_var.set("Duration: ")
    self.duration_label = Label(self.settings_window, textvariable = self.duration_label_var)
    self.duration_label.pack()

    self.duration_entry = Entry(self.settings_window)
    self.duration_entry.insert(0, self.cache["duration"])
    self.duration_entry.pack()

    self.zoom_label_var = StringVar()
    self.zoom_label_var.set("Zoom: ")
    self.zoom_label = Label(self.settings_window, textvariable = self.zoom_label_var)
    self.zoom_label.pack()

    self.zoom_entry = Entry(self.settings_window)
    self.zoom_entry.insert(0, self.cache["zoom"])
    self.zoom_entry.pack()

    self.n_harmonics_label_var = StringVar()
    self.n_harmonics_label_var.set("Number of harmonics: ")
    self.n_harmonics_label = Label(self.settings_window, textvariable = self.n_harmonics_label_var)
    self.n_harmonics_label.pack()

    self.n_harmonics_entry = Entry(self.settings_window)
    self.n_harmonics_entry.insert(0, self.cache["n_harmonics"])
    self.n_harmonics_entry.pack()

    self.fig_width_label_var = StringVar()
    self.fig_width_label_var.set("Figure width: ")
    self.fig_width_label = Label(self.settings_window, textvariable = self.fig_width_label_var)
    self.fig_width_label.pack()

    self.fig_width_entry = Entry(self.settings_window)
    self.fig_width_entry.insert(0, self.cache["fig_width"])
    self.fig_width_entry.pack()

    self.inharmonicity_label_var = StringVar()
    self.inharmonicity_label_var.set("Inharmonicity: ")
    self.inharmonicity_label = Label(self.settings_window, textvariable = self.inharmonicity_label_var)
    self.inharmonicity_label.pack()

    self.inharmonicity_entry = Entry(self.settings_window)
    self.inharmonicity_entry.insert(0, self.cache["inharmonicity"])
    self.inharmonicity_entry.pack()

    self.inharmonicity_ratio_label_var = StringVar()
    self.inharmonicity_ratio_label_var.set("Inharmonicity ratio: ")
    self.inharmonicity_ratio_label = Label(self.settings_window, textvariable = self.inharmonicity_ratio_label_var)
    self.inharmonicity_ratio_label.pack()

    self.inharmonicity_ratio_entry = Entry(self.settings_window)
    self.inharmonicity_ratio_entry.insert(0, self.cache["inharmonicity_ratio"])
    self.inharmonicity_ratio_entry.pack()

    cancel_button = Button(self.settings_window, text="Cancel", command=self.settings_window.destroy)
    cancel_button.pack()

    ok_button = Button(self.settings_window, text="OK", command= self.update)
    ok_button.pack()

  def update(self):
    self.cache["device"] = self.device.get()
    self.cache["samplerate"] = float(self.samplerate_entry.get())
    self.cache["channels"] = int(self.channels_entry.get())
    self.cache["interval"] = int(self.interval_entry.get())
    self.cache["duration"] = float(self.duration_entry.get())
    self.cache["zoom"] = float(self.zoom_entry.get())
    self.cache["n_harmonics"] = int(self.n_harmonics_entry.get())
    self.cache["fig_width"] = int(self.fig_width_entry.get())
    self.cache["inharmonicity"] = float(self.inharmonicity_entry.get())
    self.cache["inharmonicity_ratio"] = float(self.inharmonicity_ratio_entry.get())

    save_cache(self.cache)

    self.settings_window.destroy()
