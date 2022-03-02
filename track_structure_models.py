import pandas as pd
import pyamtrack.libAT as libam
import numpy as np
import matplotlib.pyplot as plt

# malloc issue
# name: list = ['']
# suc = libam.AT_RDD_name_from_number(1, name)



# material_name = 'Water, Liquid'
material_name = 'Aluminum Oxide'
material_no = libam.AT_material_number_from_name(material_name)

er_model = 6
er_model_name = libam.AT_ERModels(er_model)

particle_no = libam.AT_particle_no_from_Z_and_A_single(6, 12)
particle_name = ['']
libam.AT_particle_name_from_particle_no_single(particle_no, particle_name)

E_MeV_u = 10

# fix these
a0 = 1
rdd_parameter = [a0 * 1e-9, 0, 0]

stopping_power_source_no = libam.stoppingPowerSource_no["PSTAR"].value

RDD_models = [s.name for s in libam.RDDModels]

fig, ax = plt.subplots()
r_m = list(10**np.linspace(np.log10(1e-11), np.log(1e-3), 100))

D_RDD_Gy = len(r_m)*[0]

for RDD_name in RDD_models:
    
    rdd_model_no = libam.RDDModels[RDD_name].value

    libam.AT_D_RDD_Gy(r_m,
                      E_MeV_u,
                      particle_no,
                      material_no,
                      rdd_model_no,
                      rdd_parameter,
                      er_model,
                      stopping_power_source_no,
                      D_RDD_Gy)

    label = "{} MeV/u in {} using {}".format(E_MeV_u, material_name, RDD_name)
    label = "{}".format(RDD_name)
    ax.plot(r_m, D_RDD_Gy, label=label)

ax.set_ylim(ymin=0.1)
ax.legend()
ax.set_title("{} using '{}'".format(particle_name[0], er_model_name.name))
ax.set_xlabel("Radius (m)")
ax.set_ylabel("Dose (Gy)")
ax.set_xscale("log")
ax.set_yscale("log")
