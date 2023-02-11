import json

class Pitches():
  def __init__(self):
    self.pitches = json.loads(open("pitches.txt").read())

  def values(self):
    return self.pitches.values()

  def get_pitch_index(self, val):
    for k, v in self.pitches.items():
      if v == val:
        return int(k)
    return None

  def get_next_pitch(self, val):
    i = self.get_pitch_index(val)
    if i is not None and i < len(self.pitches):
      i += 1
    return self.pitches[str(i)]

  def get_previous_pitch(self, val):
    i = self.get_pitch_index(val)
    if i is not None and i > 0:
      i -= 1
    return self.pitches[str(i)]
