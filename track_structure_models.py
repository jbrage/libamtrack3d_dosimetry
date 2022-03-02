import pandas as pd
import pyamtrack.libAT as libam
import numpy as np
import matplotlib.pyplot as plt

# malloc issue
# name: list = ['']
# suc = libam.AT_RDD_name_from_number(1, name)

RDD_name_dic = {1: "Simple step test function",
                2: "Katz",  # "Katz' point target RDD",
                3: "Geiss",  # "Geiss' RDD [Geiss et al., 1998]",
                4: "Site",  # "Site RDD, as defined in [Edmund et al., 2007]",
                5: "Cucinotta",  # "Cucinotta, as defined in [Cucinotta et al. 1997]",
                6: "Katz Extended",  # "Katz Extended Target",
                7: "Cucinotta Extended",  # "Cucinotta Extended Target",
                8: "Radical Diffusion [Andrea Mairani]",
                }


material_name = 'Water, Liquid'
material_name = 'Aluminum Oxide'
er_model = 4

particle_no = libam.AT_particle_no_from_Z_and_A_single(6, 12)

particle_name = ['']
libam.AT_particle_name_from_particle_no_single(particle_no, particle_name)

material_no = libam.AT_material_number_from_name(material_name)

# fix these
rdd_parameter = [1e-9, 0, 0]
stopping_power_source_no = 0


fig, ax = plt.subplots()
r_m = list(10**np.linspace(np.log10(1e-11), np.log(0.1), 100))

D_RDD_Gy = len(r_m)*[0]
for E_MeV_u in [10, 250]:
    for rdd_model_no in [3, 5]:
        
        er_model_name = libam.AT_ERModels(er_model)
        rdd_model_name = RDD_name_dic[rdd_model_no]

        libam.AT_D_RDD_Gy(r_m,
                          E_MeV_u,
                          particle_no,
                          material_no,
                          rdd_model_no,
                          rdd_parameter,
                          er_model,
                          stopping_power_source_no,
                          D_RDD_Gy)

        label = "{} MeV/u, {}".format(E_MeV_u, rdd_model_name)
        ax.plot(r_m, D_RDD_Gy, label=label)

ax.legend()
ax.set_title("{} using '{}'".format(particle_name[0], er_model_name.name))
ax.set_xlabel("Radius (m)")
ax.set_ylabel("Dose (Gy)")
ax.set_xscale("log")
ax.set_yscale("log")
