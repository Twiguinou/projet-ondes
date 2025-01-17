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
B = 1.259 * 10e-14
C = 8 * 10e-29
int_lo = np.linspace(450, 750, 8)
epsilon = 1e-6
NS = 1.62
NA = 1

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
    ur = normalize(a)
    return np.arccos(np.dot(dv, np.array([ur[1], -ur[0]])))


def deviate_surface(a, dv, theta):
    ur = normalize(a)
    theta = np.pi * 0.5 - theta
    ct, st = np.cos(theta), np.sin(theta)
    if np.dot(dv, np.array([ur[1], -ur[0]])) < 0:
        rot_matrix = np.array([[ct, -st], [st, ct]])
    else:
        rot_matrix = np.array([[ct, st], [-st, ct]])
    return np.matmul(rot_matrix, dv)


def refractive_index(m, wavelength):
    if wavelength < 500:
        n = 0.1
    elif wavelength < 550:
        n = 0.2
    elif wavelength < 600:
        n = 0.3
    else:
        n = 0.4
    return (NS + n) if np.linalg.norm(m) - R < epsilon else NA


plt.style.use("dark_background")
fig, ax = plt.subplots()
ax.axis('equal')

particule = ptc.Circle((0, 0), R, facecolor='none', edgecolor='w', linewidth=2)
ax.add_patch(particule)

origin = np.array([-2, -2])
rays = [(origin, normalize(np.array([1, 1.5])), int_lo)]
white = np.array([255, 255, 255])
while len(rays) > 0:
    ray = rays.pop()
    (point, incoming_direction, wls) = ray
    cast = raycast(point, incoming_direction)
    if cast is not None:
        keep = True
    else:
        keep = False
        cast = point + normalize(incoming_direction)

    color = np.array([0, 0, 0])
    for l in wls:
        color += wavelength_to_rgb(l)
    color = np.minimum(color, white) / 255
    ax.plot((point[0], cast[0]), (point[1], cast[1]), color=color)

    theta1 = surface_angle(cast, incoming_direction)
    for wavelength in wls:
        mwl = wavelength * 10e-9
        n1, n2 = refractive_index(origin, mwl), refractive_index(cast, mwl)
        sin_theta2 = np.sin(theta1) * (n1 + mwl * 1.2e+5) / n2
        direction = incoming_direction
        if np.abs(sin_theta2) < 1:
            theta2 = np.arcsin(sin_theta2)
            if np.abs(theta2 - theta1) > epsilon:
                direction = deviate_surface(cast, direction, theta2)
        if keep:
            rays.append((cast, direction, [wavelength]))

plt.show()
