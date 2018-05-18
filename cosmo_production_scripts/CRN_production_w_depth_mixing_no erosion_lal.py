# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 12:25:57 2018

@author: LHMK
"""


import matplotlib.pyplot as plt
import numpy as np

#Method from Lal and Chen 2005 (time in years rather than seconds)
#Concentration at time zero
c_0 = 0
#Disintegration constant of the radionuclide
gam = 0
#Time (years)
t = 1000
#CRn production rate (a/g/yr)
p_0 = 5.11
#Depth (cm)
z = 40.3
#Erosion rate (cm/yr)
e = 0.01
#Density
rho = 1.8
#Attentuation length
lam = 162
#Simplified for equation (13) below
eta = gam+e/z
beta = (p_0*lam)/(rho*z)*(1-np.exp(-rho*z/lam))
delta = (p_0*e/z)*np.exp(-rho*z/lam)
yam = gam+(rho*e/lam)
#####
c_z = c_0*np.exp(-gam*t)+((beta+delta/yam)/eta)*(1-np.exp(-eta*t))-(delta/(yam*(eta-yam)))*(np.exp(-yam*t)-np.exp(-eta*t))
data2 = np.genfromtxt('C:/Workspace/github/LSDMixingModel/Runs/Model_testing/run4/p_trans_out.pout', delimiter=' ',skip_header=0, names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','c_conc','ne_conc'])

#data2 = np.genfromtxt('C:/Workspace/github/LSDMixingModel/Runs/Model_testing/run3/p_trans_out.pout', delimiter=' ',skip_header=0, names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','c_conc','ne_conc'])
#be_conc =data2['be_conc']    
#d_loc =data2['d_loc']*100
#print c_z
print c_z

be_conc =data2['be_conc']    
d_loc =data2['d_loc']    
print max(d_loc)
print np.average(be_conc)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
plt.axvline(c_z)
ax.plot(c_z,z, label = 'Lal and Chen Analytical Model')
plt.gca().invert_yaxis()
plt.tick_params(axis='both', which='major', labelsize=8)
ax.scatter(be_conc,d_loc,c='k',s= 0.1, label = 'Mixing Model')
ax.set_xlabel("CRN Concentration")
ax.set_ylabel("Soil Depth")
ax.set_xlim(0,4500)
ax.set_ylim(0.5,0)
plt.legend(loc=3,fontsize='9')
plt.savefig('crn_mixing_0.03_erosion_0.01.png', dpi=800, bbox_inches='tight') 
