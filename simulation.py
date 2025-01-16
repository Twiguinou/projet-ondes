import numpy as np
import smuthi.simulation
import smuthi.initial_field
import smuthi.layers
import smuthi.particles
import smuthi.postprocessing.graphical_output as go

d1 = 60 # épaisseur de la couche de TiO2 (nm)
n1 = 2 # indice de réfraction ^
d2 = 100 # épaisseur de la couche de SiO2 et TiO2 (nm)
n2 = 1.65 # indice de réfraction ^

nAg = 2.4

n0 = 1 # indice de réfraction de l'air
n3 = 1.5 # indice de réfraction du substrat

# SMUTHI construit les couches du bas vers le haut, les deux extrémités sont semi-infinies.
# De ce fait, le plan que définit Y=0 se trouve à l'interface entre la couche semi-infinie inférieure et la couche suivante.
# #####################
# -------- AIR --------
# D1 ---- COUCHE 1 ----
# D2 ---- COUCHE 2 ----     <- Y=+0
# ------ SUBSTRAT -----     <- Y=-0
# #####################
couches = smuthi.layers.LayerSystem(thicknesses=[0, d2, d1, 0], refractive_indices=[n3, n2, n1, n0])

def particules_matrice(radius, x_count, z_count, delta_x, delta_z, y, n):
    # top-down
    half_width = (x_count - 1) * delta_x / 2
    half_height = (z_count - 1) * delta_z / 2
    particules = []

    x_values = np.arange(-half_width, half_width + (delta_x / 2), delta_x)
    z_values = np.arange(-half_height, half_height + (delta_z / 2), delta_z)

    for x in x_values:
        for z in z_values:
            particules.append(smuthi.particles.Sphere(position=[x, y, z], refractive_index=n, radius=radius, l_max=4))
    return particules

PR = 50 # Rayon prévu des particules

# Les particules sont à l'interface entre les couches 1 et 2
particules = particules_matrice(PR, 10, 10, 180, 130, d2, nAg)

onde_initiale = smuthi.initial_field.PlaneWave(vacuum_wavelength=532, polar_angle=3*np.pi/5, azimuthal_angle=np.pi/4, polarization=0)

simulation = smuthi.simulation.Simulation(layer_system=couches, particle_list=particules, initial_field=onde_initiale, length_unit='nm')
simulation.run()

go.show_near_field(quantities_to_plot=['norm(E)', 'E_y'],
                   show_plots=True,
                   show_opts=[{'label':'raw_data'},
                              {'interpolation':'quadric'},
                              {'interpolation':'quadric'}],
                   save_plots=True,
                   save_opts=[{'format':'png'}], # animated gif of E_y
                   outputdir='./output',
                   xmin=-1000,
                   xmax=1000,
                   ymin=-200,
                   ymax=d1 + d2 + 200,
                   zmin=200,
                   zmax=200,
                   resolution_step=20,
                   simulation=simulation,
                   show_internal_field=True)
