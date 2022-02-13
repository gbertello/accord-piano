import json

from sounddevice import default

def load_pitches():
  return json.loads(open("pitches.txt").read())

def get_pitch_index(val, pitches):
  for k, v in pitches.items():
    if v == val:
      return int(k)
  return None

def get_next_pitch(val, pitches):
  i = get_pitch_index(val, pitches)
  if i is not None and i < len(pitches):
    i += 1
  return pitches[str(i)]

def get_previous_pitch(val, pitches):
  i = get_pitch_index(val, pitches)
  if i is not None and i > 0:
    i -= 1
  return pitches[str(i)]
