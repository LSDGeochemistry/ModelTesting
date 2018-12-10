# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 16:35:40 2017

@author: s0933963
"""

#Cosmo concentraion data wit hdepth based on equation A" in Brown ert al 1995 paper

import numpy as np
import matplotlib.pyplot as plt
#Load the mixing model output
data2 = np.genfromtxt('C:/Workspace/github/LSDMixingModel/Runs/Model_testing/run2/p_trans_out.pout', delimiter=' ',skip_header=0, names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','c_conc','ne_conc'])
be_conc =data2['be_conc']    
d_loc =data2['d_loc']*100
#Time (a)
t = 1000
#Production rate at surface (atoms/g/a) (taken from Table 6)
p_0 = 5.11 #from LSD mixing model
#Depth of profile (cm)
d = max(d_loc)
#Depth profile for testing
z = np.arange(0,d,0.01)
#density of material (g/cm^3)
rho = 1.8
#density of quartz (g/cm^3)
rho_q =2.2
#Decay Constant
gamma = 500*np.power(10.0,-9) 
#attenuation lenth (g/cm^2)
l = 160 #from the LSD mixing model

#Assuming full mixing across the column find the average production rate
#From Brown
p_ave = (p_0/(d*l**-1))*(1-np.exp(-d*l**-1))
p = p_ave*t
mixed = p-(p*gamma*t)
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
#ax.plot(p_z_t,z)
plt.axvline(mixed, label = 'Lal and Chen Analytical Model')
print np.average(be_conc)
print mixed
ax.scatter(be_conc,d_loc,c='k',s= 0.4, label = 'Mixing Model')
ax.set_xlabel("CRN Concentration")
ax.set_ylabel("Soil Depth")
ax.set_xlim(0,max(be_conc))
ax.set_ylim(min(d_loc),max(d_loc))
plt.gca().invert_yaxis()
plt.legend(loc=3,fontsize='9')
plt.savefig('crn_no_erosion_full_mixing.png', dpi=800, bbox_inches='tight')
