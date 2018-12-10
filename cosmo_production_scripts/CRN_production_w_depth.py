# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 16:35:40 2017

@author: s0933963
"""

#Cosmo concentraion data with depth based on equation 20 in Niedermann, 2002 paper

import numpy as np
import matplotlib.pyplot as plt
#Time (a)
t = 1000
#Production rate at surface (atoms/g/a) (taken from Table 6)
p_0 = 5.11 #from LSD mixing model
#Depth of profile (cm)
d = 50
#Depth profile for testing
z = np.arange(0,d,0.1)
#density of material (g/cm^3)
rho = 1.8
#density of quartz (g/cm^3)
rho_q =2.65
e = 0
#Decay Constant
gamma = 0 
#attenuation lenth (g/cm^2)
l = 160 #from the LSD mixing model
#Production rate at different depth each year
p_z = p_0*np.exp(-rho*z/l)
#Production for x number of years
p_z_t = p_z*t
#print p_z_t
#Load the mixing model output
data2 = np.genfromtxt('C:/Workspace/github/LSDMixingModel/Runs/Model_testing/run1/p_trans_out.pout', delimiter=' ',skip_header=0, names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','c_conc','ne_conc'])
be_conc =data2['be_conc']    
d_loc =data2['d_loc']*100

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(p_z_t,z,label = 'Lal and Chen Analytical Model')
ax.scatter(be_conc,d_loc,c='k',s= 0.4, label = 'Mixing Model')

ax.set_xlabel("CRN Concentration")
ax.set_ylabel("Soil Depth")
ax.set_xlim(0,5500)
ax.set_ylim(0,50)
plt.gca().invert_yaxis()
plt.legend(loc=3,fontsize='9')
plt.savefig('crn_no_erosion_no_mixing.png', dpi=800, bbox_inches='tight')