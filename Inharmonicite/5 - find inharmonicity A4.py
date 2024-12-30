#!/usr/bin/env python3

from common import get_stiffness
import numpy as np
import matplotlib.pyplot as plt
import math

max_harmonics = 4
B = get_stiffness(49, 1, max_harmonics)
I = 200 * math.log2((1 + 4 * B) / (1 + B))

print(I)