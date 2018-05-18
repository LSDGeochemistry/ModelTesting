# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 16:35:40 2017

@author: s0933963
"""

#Cosmo concentraion data wit hdepth based on equation 20 in Niedermann, 2002 paper

import numpy as np
import matplotlib.pyplot as plt
#Time (a)
t = 1000
#Production rate at surface (atoms/g/a) (taken from Table 6)
p_0 = 5.11 #from LSD mixing model
#Depth of profile (cm)
d = 50.3
#Depth profile for testing
z = np.arange(0,d,0.1)
#density of material (g/cm^3)
rho = 1.8
#density of quartz (g/cm^3)
rho_q =2.2
#Erosion Rate
e = 0
#Decay Constant
gamma = 0 
#attenuation lenth (g/cm^2)
l = 162
#Production rate at different depth each year
p_z = p_0*np.exp(-rho*z/l)
#Production for x number of years
p_z_t = p_z*t
#print p_z_t
#Concentration over this time period including erosion (rearranged equation 33 from Niedermann)
c_z_t = (p_z_t*l)/(rho_q*(e+(l*gamma)/rho_q))
#print c_z_t
mixed =  np.average(p_z_t)
print (mixed)
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(p_z_t,z)
plt.axvline(mixed)
plt.gca().invert_yaxis()
ax.set_xlabel("CRN Concentration")
ax.set_ylabel("Soil Depth")
ax.set_xlim(0,5500)
#plt.savefig('crn_no_mixing.png', dpi=800, bbox_inches='tight')
