# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 13:44:21 2018

@author: LHMK
"""

# CRN concentration as a function of depth, incorporatin bioturbation
import numpy as np
import matplotlib.pyplot as plt
#Variables
#time (years)
t = 1000
#depth (cm)
d = 60
#depth profile for testing (cm)
z = np.arange(0,d,1)
#density (g/cm^3)
rho = 1.8
#overlying mass (g/cm^2)
x = z*rho
#Surface produciton rate (atoms/g/a)
p = 5.11
#Effective attenutaion length (g/cm^2)
l = 162
#Radioactive decay constant (a)
lm = 0
#Erosion rate (g/cm^2/a)
e = 0.1
#Bioturbation depth (cm) 
b = 60
#Part of profile not affected by Bioturbation
x_b = x
#Brown method for bioturbated soil
N = ((l*np.exp(-x_b*l**-1))/(l-x_b))*((p/(e*l**-1+lm))*(1-np.exp(-t*(e*l**-1+lm))))+(1-(l*np.exp(-x_b*l**-1))/(l-x_b))*((p/(e*l**-1+lm*x_b*l**-1))*(1-np.exp(-t*(e*x_b**-1+lm))))
#Changes it so the negative concentration equal 0 instead
#print N
N=N.clip(min=0)
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(N,z)
plt.gca().invert_yaxis()
ax.set_xlabel("CRN Concentration")
ax.set_ylabel("Soil Depth")
ax.set_xlim(0,5500)
