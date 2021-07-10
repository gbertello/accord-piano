import os
import json
from pitches import get_pitch_index

def load_cache():
  cache = {}
  if os.path.exists("cache.json"):
    with open("cache.json") as f:
      cache = json.loads(f.read())
  if "duration" not in cache.keys():
    cache["duration"] = 20
  if "zoom" not in cache.keys():
    cache["zoom"] = 0.05
  if "pitch" not in cache.keys():
    cache["pitch"] = "LA4"
  if "harmonics" not in cache.keys():
    cache["harmonics"] = {}
  if "n_harmonics" not in cache.keys():
    cache["n_harmonics"] = 8
  if "fig_width" not in cache.keys():
    cache["fig_width"] = 2
  if "inharmonicity" not in cache.keys():
    cache["inharmonicity"] = 0
  if "inharmonicity_ratio" not in cache.keys():
    cache["inharmonicity_ratio"] = 1
  return cache

def show_cache(cache):
  print("Duration: %s" % cache["duration"])
  print("Pitch: %s" % cache["pitch"])
  print("Zoom: %s" % cache["zoom"])
  print("Inharmonicity: %s" % cache["inharmonicity"])
  print("Inharmonicity ratio: %s" % cache["inharmonicity_ratio"])
  print("Inharmonicity progress factor: %s" % cache["inharmonicity_progress_factor"])

def show_cache_harmonics(cache, pitches):
  print("Harmonics:")
  for pitch in sorted([i for i in cache['harmonics'].keys()]):
    print(("%s (%s): " % (pitch, pitches[pitch])).ljust(12) + "%s" % cache['harmonics'][pitch])

def store_duration_in_cache(cache, val):
  if not is_number(val):
    print("duration should be a decimal number")
    return
  duration = float(val)
  cache['duration'] = duration
  print("duration set to %s" % duration)

def is_number(val):
  if val.replace(".", "").isdigit():
    return True
  else:
    return False

def is_pitch_string(val, pitches):
  if val in pitches.values():
    return True
  else:
    return False

def store_pitch_in_cache(cache, val, pitches):
  if not is_pitch_string(val, pitches):
    print("pitch should be a pitch string (e.g. \"LA4\")")
    return
  pitch = val
  cache['pitch'] = pitch
  print("pitch set to %s" % pitch)

def store_zoom_in_cache(cache, val):
  if not is_number(val):
    print("zoom should be a decimal number")
    return
  zoom = float(val)
  cache['zoom'] = zoom
  print("zoom set to %s" % zoom)

def store_number_of_harmonics_in_cache(cache, val):
  if not is_number(val):
    print("number of harmonics should be an integer")
    return
  n_harmonics = int(val)
  cache["n_harmonics"] = n_harmonics
  print("number of harmonics set to %s" % n_harmonics)

def store_figure_width_in_cache(cache, val):
  if not is_number(val):
    print("figure width should be an integer")
    return
  fig_width = int(val)
  cache["fig_width"] = fig_width
  print("figure width set to %s" % fig_width)

def store_inharmonicity_in_cache(cache, val):
  if not is_number(val):
    print("inharmonicity should be a number")
    return
  inharmonicity = float(val)
  cache["inharmonicity"] = inharmonicity
  print("inharmonicity set to %s" % inharmonicity)

def store_inharmonicity_ratio_in_cache(cache, val):
  if not is_number(val):
    print("inharmonicity ratio should be a number")
    return
  inharmonicity_ratio = float(val)
  cache["inharmonicity_ratio"] = inharmonicity_ratio
  print("inharmonicity ratio set to %s" % inharmonicity_ratio)

def store_inharmonicity_progress_factor_in_cache(cache, val):
  if not is_number(val):
    print("inharmonicity progress factor width should be a number")
    return
  inharmonicity_progress_factor = float(val)
  cache["inharmonicity_progress_factor"] = inharmonicity_progress_factor
  print("inharmonicity progress factor set to %s" % inharmonicity_progress_factor)

def delete_harmonic_in_cache(cache, val, pitches):
  if not is_pitch_string(val, pitches):
    print("pitch should be a pitch string (e.g. \"LA4\")")
    return
  pitch = val
  p = get_pitch_index(pitch, pitches)
  if str(p) in cache['harmonics'].keys():
    del(cache['harmonics'][str(p)])
    print("harmonic %s deleted" % pitch)

def delete_all_harmonics_in_cache(cache):
  print("Are you sure to delete cache harmonics? (y/N)")
  confirm = input()
  if confirm.lower() == "y":
    cache["harmonics"] = {}
    print("cache erased")
