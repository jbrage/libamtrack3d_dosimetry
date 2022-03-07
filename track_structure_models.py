import pandas as pd
import pyamtrack.libAT as libam
import numpy as np
import matplotlib.pyplot as plt


# define the parameters as in 
# "Greilich, S., Grzanka, L., Bassler, N., Andersen, C. E., & Jäkel, O. (2010). Amorphous track models: a numerical comparison study. Rad Meas, 45(10), 1406-1409."
material_name = 'Aluminum Oxide'
E_MeV_u = 10
particle_no = libam.AT_particle_no_from_Z_and_A_single(6, 12)

"""
Problems:
* I would like to get the core/site radius a0 for each of the RDD, but encounter an error with
	libam.AT_RDD_a0_m() 
  "module 'pyamtrack.libAT' has no attribute 'AT_RDD_a0_m'"

  so how I get a0 for a given RDD model?
  
* How do I determine which ER model is suitable for the given RDD?

"""

# these should be corrected:
a0_m = 1e-9
er_model = 6

# get the material number
material_no = libam.AT_material_number_from_name(material_name)

# get the ER name
er_model_name = libam.AT_ERModels(er_model)

# get the particle name 
particle_name = ['']
libam.AT_particle_name_from_particle_no_single(particle_no, particle_name)

# get the stopping power
stopping_power_source_no = libam.stoppingPowerSource_no["PSTAR"].value

# prepare plot
fig, ax = plt.subplots()
r_m = list(10**np.linspace(np.log10(1e-10), np.log(1e-1), 1000))
D_RDD_Gy = len(r_m)*[0]

# plot each RDD
for RDD_model in libam.RDDModels:
    
    rdd_model_no = RDD_model.value
    
    # AttributeError: module 'pyamtrack.libAT' has no attribute 'AT_RDD_a0_m'
    # test = [0, 0, 0]
    # print(libam.AT_RDD_a0_m(1e-7, rdd_model_no, test))
    
    # create a list of the right length (probably not necessary?)
    n_rdd_parameters = libam.AT_RDD_number_of_parameters(rdd_model_no)
    rdd_parameter = [0] * n_rdd_parameters
    if rdd_parameter:
        rdd_parameter[0] = a0_m # is this correct at all?

    libam.AT_D_RDD_Gy(r_m,
                      E_MeV_u,
                      particle_no,
                      material_no,
                      rdd_model_no,
                      rdd_parameter,
                      er_model,
                      stopping_power_source_no,
                      D_RDD_Gy)

    label = "{}".format(RDD_model.name.replace("RDD_", ""))
    ax.plot(r_m, D_RDD_Gy, label=label)

ax.set_ylim(ymin=0.1)
ax.legend()
ax.set_title("{} using '{}'".format(particle_name[0], er_model_name.name))
ax.set_xlabel("Radius (m)")
ax.set_ylabel("Dose (Gy)")
ax.set_xscale("log")
ax.set_yscale("log")
