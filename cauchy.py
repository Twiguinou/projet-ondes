import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as ptc

R = 1
int_lo = np.linspace(400, 700, 10)

def raytrace(start, direction):
    s = np.dot(start, direction)
    nd2 = np.dot(start, start)
    na2 = np.dot(direction, direction)
    c1 = s / nd2
    c2 = np.sqrt((s * c1 - na2 + R * R) / nd2)
    t1 = -c1 + c2
    t2 = -c1 - c2

fig, ax = plt.subplots()
ax.axis('equal')

particule = ptc.Circle((0, 0), R, facecolor='none', edgecolor='r', linewidth=2)
ax.add_patch(particule)

ax.plot((2), (2), 'o', color='y')

plt.show()
