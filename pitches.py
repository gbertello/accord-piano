import json

from sounddevice import default

def load_pitches():
  return json.loads(open("pitches.txt").read())

def get_pitch_index(val, pitches):
  for k, v in pitches.items():
    if v == val:
      return int(k)
  return None
