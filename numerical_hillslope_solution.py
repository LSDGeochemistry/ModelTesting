# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 14:14:50 2018

@author: LHMK
"""
#Model showing the basic analytical soltion for hillslope evolution
import matplotlib.pyplot as plt
import numpy as np
#
W_0 = 2.5*np.power(10.0,-7)
#
gamma = 1*np.power(10.0,9)
#Uplift Rate (m)
U = 0
#Density of soil (kg/m^3)
rho = 1000
#Diffusivity (m/yr)
k = 0.012
#Time
t = 10
#Initialise a hillslope
width = np.ones(50)
length = np.arange(0,50,1)
depth = np.random.rand(50,1.0)
d_depth = np.zeros_like(depth,dtype=float)
n_depth = np.zeros_like(depth,dtype=float)
set_elevation = np.arange(100,110,0.2)
elevation = set_elevation[::-1]
flux = np.arange(0,50,1.0)
s = np.zeros_like(depth)
depth_print = []
#Counter for Printing
count = 0
#print elevation
#print width
#print length
#print depth

#area = width*depth
#print area
for i in range (0,t):
    for j in range (1,50):
        flux[j] = -rho*k*width[j-1]*depth[j-1]*(((elevation[j-1]-elevation[j])/(length[j-1]-length[j])))
        
        #Convert the flux to a depth
        d_depth[j] = flux[j]/rho/k/width[j-1] 
        
        
        if d_depth[j] <=0:
            d_depth[j] = 0
        #print d_depth[j]
        #print depth[j-1]
        
        n_depth[j-1] = depth[j-1]-d_depth[j]
        #print n_depth[j-1]
        
        n_depth[j] = depth[j]+d_depth[j]
        depth[j-1] = n_depth[j-1]
        depth[j] = n_depth[j]
    #Factor in SOil production
        s[j-1] = W_0*np.exp(-depth[j-1]*gamma)
        print depth[j-1]
        print s[j-1]
        depth [j-1] = depth[j-1]+s[j-1]
    #print depth
    if count == 100:
        depth_print_line = str(i)+" "+str(depth)+"\n"
        depth_print.append(depth_print_line)
        count = 0
        
    else: 
        print count
        count = count+1   

#print depth_print
#Print FIles for analysis
filename = "HIllslope profiles, 0 to "+str(t)+".txt"
f = open(filename, 'w')        
f.writelines(depth_print)
f.close()
   
        
        
        
        
        
    




