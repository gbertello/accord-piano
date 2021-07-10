#!/usr/bin/env python3

def f(f0, k):
  return f0 * 2 ** ((k - 49) / 12)

def fk(f, k, n, I, q):
  return n * f * 2 ** (((n ** 2 - 1) * I * q ** (k - 49)) / 1200)

def get_lower_octave(f, k, I, q):
  n = 2
  return f / n / 2 ** (((n ** 2 - 1) * I * q ** (k - 12 - 49)) / 1200)

def corrected_f(f1, f2, coef):
  return f * (1 - coef) + f2 * coef

f0 = 440
I = 0.58
q = 1.085
coef = 0.6
factor = 1.00008

#for k in range(1, 89):
#  print(k, round(f(f0, k), 2), round(corrected_f2(f(f0, k), k, factor), 2), round(corrected_f(f(f0, k), k, I, q, coef), 2), round(fk(f(f0, k - 12), k - 12, 2, I, q), 2))

LA4 = f(f0, 49)
LA4_2 = fk(LA4, 49, 2, I, q)

def corrected_f3(f0, k):
  l = (1 + coef * (2 ** (3 * I / 1200) - 1)) ** (1 / 12)
  return f(f0, k) * l ** (k - 49)

for k in range(1, 89):
  print(k, round(f(f0, k), 2), round(corrected_f3(f0, k), 2))
