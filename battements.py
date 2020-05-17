import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

fig = plt.figure(figsize=(12,4))
ax = fig.add_subplot()
#tmax = 0.0002
tmax = 0.0018
c = 350

ech = 10000
t = np.linspace (0, tmax, ech)
E1 = np.linspace(0, 0, ech)
E2 = np.linspace(0, 0, ech)
f1 = 40000.
f2 = 42000.
w1 = 2. * np.pi * f1
w2 = 2. * np.pi * f2
for e in range(ech):
    E1[e]=np.cos(w1*t[e])
    E2[e]=np.cos(w2*t[e])

#plt.plot(t, E1)
#plt.plot(t, E2)
plt.plot(t, E1 + E2)

#print("f1 = ", f1, "(s-1)")
#print("f2 = ", f2, "(s-1)")

plt.show()


#Calcul de la vitesse de l'onde
d = 0.0425
n = 5
la = d/n
c = la * f1
s_exp = c * np.sqrt(np.square(0.001/d))
print("vitesse de l'onde : ", c, "(m.s-1)")
print("incertitude sur la vitesse de l'onde : ", s_exp, "(m.s-1)")


#calcul vitesse du train
sT = 0.00024
fm = f2 - f1
vitesse_emetteur = c*fm/(fm+f1)
print("vitesse de l'Ã©metteur = ", vitesse_emetteur, " (m.s-1)")
sv_exp = vitesse_emetteur*np.sqrt(np.square(sT*fm)+ np.square(s_exp/c))
print("incertitude sur la vitesse de l'Ã©metteur : ", sv_exp, "(m.s-1)")
