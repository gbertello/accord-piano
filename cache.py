import os
import json
import sounddevice as sd

class Cache():
  def __init__(self):
    self.cache = {}
    self.reset()

  def reset(self):
    if os.path.exists("cache.json"):
      with open("cache.json") as f:
        self.cache = json.loads(f.read())

    devices = [d['name'] for d in sd.query_devices()]
    if len(devices) == 0:
        print("No sound device exists")
        exit()
    if "device" not in self.cache.keys() or self.get("device") not in devices:
      self.set("device", devices[0])

    if "channels" not in self.cache.keys():
      self.set("channels", 1)
    if "samplerate" not in self.cache.keys():
      self.set("samplerate", 192000)
    if "duration" not in self.cache.keys():
      self.set("duration", 5)
    if "zoom" not in self.cache.keys():
      self.set("zoom", 0.08)
    if "pitch" not in self.cache.keys():
      self.set("pitch", "LA4")
    if "harmonics" not in self.cache.keys():
      self.set("harmonics", {})
    if "n_harmonics" not in self.cache.keys():
      self.set("n_harmonics", 6)
    if "fig_width" not in self.cache.keys():
      self.set("fig_width", 3)
    if "inharmonicity" not in self.cache.keys():
      self.set("inharmonicity", 0)
    if "inharmonicity_ratio" not in self.cache.keys():
      self.set("inharmonicity_ratio", 1)
    if "interval" not in self.cache.keys():
      self.set("interval", 30)

  def get(self, key):
    return self.cache[key]

  def set(self, key, val):
    self.cache[key] = val

  def save(self):
    with open('cache.json', 'w') as f:
      f.write(json.dumps(self.cache, indent=2))

  def delete_harmonic(self, val, pitches):
    p = pitches.get_pitch_index(val)
    harmonics = self.get('harmonics')
    if str(p) in harmonics.keys():
      del(harmonics[str(p)])
      self.set('harmonics', harmonics)
      self.save()

  def delete_all_harmonics(self):
    self.set('harmonics', {})
    self.save()
