import json

class Pitches():
  def __init__(self):
    self.pitches = PITCHES

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

PITCHES = {
  "1": "LA0",
  "2": "LA#0",
  "3": "SI0",
  "4": "DO1",
  "5": "DO#1",
  "6": "RE1",
  "7": "RE#1",
  "8": "MI1",
  "9": "FA1",
  "10": "FA#1",
  "11": "SOL1",
  "12": "SOL#1",
  "13": "LA1",
  "14": "LA#1",
  "15": "SI1",
  "16": "DO2",
  "17": "DO#2",
  "18": "RE2",
  "19": "RE#2",
  "20": "MI2",
  "21": "FA2",
  "22": "FA#2",
  "23": "SOL2",
  "24": "SOL#2",
  "25": "LA2",
  "26": "LA#2",
  "27": "SI2",
  "28": "DO3",
  "29": "DO#3",
  "30": "RE3",
  "31": "RE#3",
  "32": "MI3",
  "33": "FA3",
  "34": "FA#3",
  "35": "SOL3",
  "36": "SOL#3",
  "37": "LA3",
  "38": "LA#3",
  "39": "SI3",
  "40": "DO4",
  "41": "DO#4",
  "42": "RE4",
  "43": "RE#4",
  "44": "MI4",
  "45": "FA4",
  "46": "FA#4",
  "47": "SOL4",
  "48": "SOL#4",
  "49": "LA4",
  "50": "LA#4",
  "51": "SI4",
  "52": "DO5",
  "53": "DO#5",
  "54": "RE5",
  "55": "RE#5",
  "56": "MI5",
  "57": "FA5",
  "58": "FA#5",
  "59": "SOL5",
  "60": "SOL#5",
  "61": "LA5",
  "62": "LA#5",
  "63": "SI5",
  "64": "DO6",
  "65": "DO#6",
  "66": "RE6",
  "67": "RE#6",
  "68": "MI6",
  "69": "FA6",
  "70": "FA#6",
  "71": "SOL6",
  "72": "SOL#6",
  "73": "LA6",
  "74": "LA#6",
  "75": "SI6",
  "76": "DO7",
  "77": "DO#7",
  "78": "RE7",
  "79": "RE#7",
  "80": "MI7",
  "81": "FA7",
  "82": "FA#7",
  "83": "SOL7",
  "84": "SOL#7",
  "85": "LA7",
  "86": "LA#7",
  "87": "SI7",
  "88": "DO8"
}
