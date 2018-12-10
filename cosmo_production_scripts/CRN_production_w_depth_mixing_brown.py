# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 13:44:21 2018

@author: LHMK
"""

# CRN concentration as a function of depth, incorporatin bioturbation
import numpy as np
import matplotlib.pyplot as plt
data2 = np.genfromtxt('C:/Workspace/github/LSDMixingModel/Runs/Model_testing/run4/p_trans_out.pout', delimiter=' ',skip_header=0, names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','c_conc','ne_conc'])

be_conc =data2['be_conc']    
d_loc =data2['d_loc']

#Variables
#time (years)
t = 1000
#depth (cm)
d = max(d_loc)*100
#depth profile for testing (cm)
z = np.arange(0,d,0.1)
#density (g/cm^3)
rho = 1.8
#overlying mass (g/cm^2)
x = z*rho
#Surface produciton rate (atoms/g/a)
p = 5.11
#Effective attenutaion length (g/cm^2)
l = 160
#Radioactive decay constant (a)
lm = gam = 500*np.power(10.0,-9)  
#Erosion rate (g/cm^2/a)
e = 0.01*rho
#Bioturbation depth (cm) 
b = d
#Part of profile affected by Bioturbation
x_b = d
#Brown method for bioturbated soil
N = ((l*np.exp(-x_b*l**-1))/(l-x_b))*((p/(e*l**-1+lm))*(1-np.exp(-t*(e*l**-1+lm))))+(1-(l*np.exp(-x_b*l**-1))/(l-x_b))*((p/(e*l**-1+lm*x_b*l**-1))*(1-np.exp(-t*(e*x_b**-1+lm))))
#Changes it so the negative concentration equal 0 instead

print N

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.plot(N, label = 'Lal and Chen Analytical Model')
plt.gca().invert_yaxis()
plt.tick_params(axis='both', which='major', labelsize=8)
ax.scatter(be_conc,d_loc,c='k',s= 0.1, label = 'Mixing Model')
ax.set_xlabel("CRN Concentration")
ax.set_ylabel("Soil Depth")
ax.set_xlim(0,max(be_conc))
ax.set_ylim(0.5,0)
plt.legend(loc=3,fontsize='9')
#plt.savefig('crn_mixing_0.03_erosion_0.01.png', dpi=800, bbox_inches='tight') 