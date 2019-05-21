# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 16:45:05 2018

@author: LHMK
"""

import matplotlib.pyplot as plt
import numpy as np

#Method from Lal and Chen 2005 (time in years rather than seconds)
#Concentration at time zero
c_0 = 0
#Disintegration constant of the radionuclide
gam = 500*np.power(10.0,-9)
#Time (years)
t = 1000
#CRn production rate (a/g/yr)
p_0 = 5.11
#Depth (cm)
z = np.arange(0,50,0.1)
#Erosion rate (cm/yr)
e = 0.01
#Density
rho = 1.8
#Attentuation length
lam = 160


#####
c_z = c_0*np.exp(-gam*t)+((p_0*np.exp(-rho*z/lam))/(gam+rho*e/lam))*(1-np.exp(-t*(gam+rho*e/lam)))

data2 = np.genfromtxt('C:/Workspace/github/LSDMixingModel/Runs/Model_testing/run3/p_trans_out.pout', delimiter=' ',skip_header=0, names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','c_conc','ne_conc'])
be_conc =data2['be_conc']    
d_loc =data2['d_loc']*100
print max(d_loc)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(c_z,z, label = 'Lal and Chen Analytical Model')
plt.gca().invert_yaxis()
plt.tick_params(axis='both', which='major', labelsize=8)
ax.scatter(be_conc,d_loc,c='k',s= 1.0, label = 'Mixing Model')
ax.set_xlabel("CRN Concentration")
ax.set_ylabel("Soil Depth")
#ax.set_xlim(0,5500)
ax.set_ylim(60,0)
plt.legend(loc=3,fontsize='9')
plt.savefig('crn_erosion_no_mixing.png', dpi=800, bbox_inches='tight')