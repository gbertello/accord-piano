#!/usr/bin/env python3
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

x=np.array(range(0, 21))
y=np.array([0, 440.0, 876.4, 1323.4, 1768.6, 2216.6, 2523.8, 2956.0, 3364.8, 3769.4, 4471.8, 4641.2, 5541.0, 5650.4, 6432.8, 6822.8, 6822.8, 7275.2, 8194.2, 8520.8, 8520.8])

x = x[:,np.newaxis]
a, _, _, _ = np.linalg.lstsq(x, y, rcond=None)

print(a)

plt.plot(x, y, 'bo')
plt.plot(x, a*x, 'r-')
plt.show()

