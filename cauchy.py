import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as ptc

def wavelength_to_rgb(wavelength, gamma=0.8):
    if 380 <= wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        r = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        g = 0.0
        b = (1.0 * attenuation) ** gamma
    elif 440 <= wavelength <= 490:
        r = 0.0
        g = ((wavelength - 440) / (490 - 440)) ** gamma
        b = 1.0
    elif 490 <= wavelength <= 510:
        r = 0.0
        g = 1.0
        b = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif 510 <= wavelength <= 580:
        r = ((wavelength - 510) / (580 - 510)) ** gamma
        g = 1.0
        b = 0.0
    elif 580 <= wavelength <= 645:
        r = 1.0
        g = (-(wavelength - 645) / (645 - 580)) ** gamma
        b = 0.0
    elif 645 <= wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        r = (1.0 * attenuation) ** gamma
        g = 0.0
        b = 0.0
    else:
        r = 0.0
        g = 0.0
        b = 0.0
    return np.array([int(r * 255), int(g * 255), int(b * 255)])

def normalize(a):
    return a / np.linalg.norm(a)

R = 1
int_lo = np.linspace(400, 700, 10)
epsilon = 1e-6

def raycast(start, dv):
    s = np.dot(start, dv)
    n = np.dot(start, start) - R * R
    d2 = np.dot(dv, dv)
    c1 = s / d2
    delta2 = s * c1 - n

    if delta2 > epsilon:
        c2 = np.sqrt(delta2 / d2)
        if -c1 - c2 > epsilon:
            t = -c1 - c2
        elif -c1 + c2 > epsilon:
            t = -c1 + c2
        else:
            return None

        return start + dv * t

    return None

def surface_angle(a, dv):


fig, ax = plt.subplots()
ax.axis('equal')

particule = ptc.Circle((0, 0), R, facecolor='none', edgecolor='r', linewidth=2)
ax.add_patch(particule)

rays = [(np.array([-2, -2]), normalize(np.array([1, 1])), int_lo)]
while len(rays) > 0:
    ray = rays.pop()
    (point, direction, wls) = ray
    cast = raycast(point, direction)

    if cast is not None:
        color = np.array([0, 0, 0])
        for l in wls:
            color += wavelength_to_rgb(l)
        color = np.minimum(color, np.array([255, 255, 255])) / 255

        ax.plot((point[0],cast[0]), (point[1],cast[1]), color=color)
        rays.append((cast, direction, wls))

plt.show()
