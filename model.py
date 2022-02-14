#!/usr/bin/env python3

# I = 1200 * (math.log2(880.9) - math.log2(880)) / 3
# q = (0.59 / 0.446) ^ (1/12)

def get_pure_frequency(p, n):
  return 440 * (2 ** ((p - 49) / 12)) * n

# Model 1: on 1st partial
def get_corrected_frequency_1(p, I, q):
  corrected_frequency = 440

  i = 49
  while i > 12:
    corrected_frequency = corrected_frequency / 2 / (1 + (2 ** ((3 * I * ((q ** (i - 12 - 49)) / 1200))) - 1))
    i -= 12

  while i < (p - 1) % 12 + 1:
    corrected_frequency = corrected_frequency * 2 ** (1 / 12)
    i += 1

  while i < p:
    corrected_frequency = 2 * corrected_frequency * (1 + (2 ** ((3 * I * ((q ** (i - 49)) / 1200))) - 1))
    i += 12

  return corrected_frequency

# Model 2: On 2nd partial
def get_corrected_frequency_2(p, I, q):
  corrected_frequency = 440

  i = 49
  while i > 6:
    corrected_frequency = corrected_frequency / 2 ** (7/12) / 2 ** ((8 * I * q ** (i - 49 - 7) - 3 * I * q ** (i - 49)) / 1200)
    i -= 7

  while i < (p - 1) % 7 + 1:
    corrected_frequency = corrected_frequency * 2 ** (1 / 12)
    i += 1

  while i < p:
    corrected_frequency = corrected_frequency * 2 ** (7/12) * 2 ** ((8 * I * q ** (i - 49) - 3 * I * q ** (i - 49 + 7)) / 1200)
    i += 7

  return corrected_frequency

# Model 3: on 3rd partial
def get_corrected_frequency_3(p, I, q):
  corrected_frequency = 440

  i = 49
  while i > 12:
    corrected_frequency = corrected_frequency / 2 / 2 ** ((15 * I * q ** (i - 49 - 12) - 3 * I * q ** (i - 49)) / 1200)
    i -= 12

  while i < (p - 1) % 12 + 1:
    corrected_frequency = corrected_frequency * 2 ** (1 / 12)
    i += 1

  while i < p:
    corrected_frequency = corrected_frequency * 2 * 2 ** ((15 * I * q ** (i - 49) - 3 * I * q ** (i - 49 + 12)) / 1200)
    i += 12

  return corrected_frequency


if __name__ == "__main__":
  for p in range(1, 89):
    print(p, get_corrected_frequency_2(p, 0.58, 1.085))