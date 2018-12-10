# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 14:14:50 2018

@author: LHMK
"""
#Model showing the basic analytical soltion for hillslope evolution
import numpy as np
#Production when no soil (in m/yr)
W_0 = 1*np.power(10.0,-4)
#scaling factor for decreasing soil produciton with increasing depth
gamma = 0.5
#Uplift Rate (m) ****not used****
U = 0
#Density of soil (kg/m^3)
rho = 1000
#Sediment transport coefficient (diffusivity?) (m/yr) in the simple linear flux law values taken from (Roering 2008)
k_1 = 0.005
k_2 = 0.012
#Time of Model (yr)
t = 5000
#Number of nodes (for simplicity each node represents a 1m interval)
nodes = 50
#Elevation of top and bottom of hillslope (m)
z_1 = 110
z_2 = 100
#Get the distance for each node
d_z = float(z_1-z_2)/nodes 
###Initialise a hillslope
#Sets the widths in m
width = np.arange(0,nodes,dtype=float)
width.fill(0.1)
#Creates a length of x nodes
length = np.arange(0,nodes,1)

######2 options for the depths
#Sets the inital starting depths as betewen 0 and 1m
#depth = np.random.rand(nodes,1.0)
#Sets all depths to a fixed value
depth = np.arange(0,nodes,dtype=float)
depth.fill(0.5)

#Used in the loops for getting new depths
d_depth = np.zeros_like(depth,dtype=float)
n_depth = np.zeros_like(depth,dtype=float)
#Creates the elevation changes
set_elevation = np.arange(z_2,z_1,d_z)
#Flip the elevation array so it goes from high to low
elevation = set_elevation[::-1]
#Set up an array to be populated with fluxes
flux = np.arange(0,nodes,1.0)
#Linear sediment flux
q_s = np.arange(0,nodes,1.0)
#Slope dependent linear sediment flux
q_s_s = np.arange(0,nodes,1.0)
#Set up array to be filled with soil production rates 
s = np.zeros_like(depth)
#Set up an array to append values to
depth_print = []
#Counter for Printing
count = 0
#Various test statements for printing
#print elevation
#print width
#print length
#print depth
#area = width*depth
#print area
#Now loop through the hillslope
for i in range (0,t):
    for j in range (1,nodes):
        #Get the flux using a simple linear sediment flux law
        flux[j] = -rho*k_2*width[j-1]*depth[j-1]*((elevation[j-1]-elevation[j])/(length[j-1]-length[j]))
        #Convert the flux to a depth
        d_depth[j] = flux[j]/rho/d_z/width[j-1] 
        #Calculate the other fluxes
        q_s[j] = -k_1*((elevation[j-1]-elevation[j])/(length[j-1]-length[j]))
        q_s_s[j] = -k_2*depth[j-1]*np.cos((elevation[j-1]-elevation[j])/np.sqrt((elevation[j-1]-elevation[j])**2+(length[j-1]-length[j])**2))*((elevation[j-1]-elevation[j])/(length[j-1]-length[j]))
        #Compare fluxes:
#        print 'model flux',flux[j]/rho/width[j-1]
#        print 'linear flux',q_s[j]
#        print 'depth-slope flux',q_s_s[j]
        #Set the depth so it can't de negative (this shouldn't happen if the code is working properly)
        if d_depth[j] <=0:
            d_depth[j] = 0
        #print d_depth[j]
        #print depth[j-1]
        #Find the new depths based on the converted flux 
        n_depth[j-1] = depth[j-1]-d_depth[j]
        #print n_depth[j-1]
        n_depth[j] = depth[j]+d_depth[j]
        depth[j-1] = n_depth[j-1]
        depth[j] = n_depth[j]
    #Factor in SOil production
        s[j-1] = W_0*np.exp(-depth[j-1]/gamma)
        #print depth[j-1]
        #print s[j-1]
        depth [j-1] = depth[j-1]+s[j-1]
    #print depth at whatever intervals (here every 100 years)
    if count == 100:
        depth_print_line = str(i)+" "+str(depth)+"\n"
        depth_print.append(depth_print_line)
        count = 0
        
    else: 
        #print count
        count = count+1   

#print depth_print
#Create the output file, probs a bterr way to do this 
filename = "HIllslope profiles, 0 to "+str(t)+".txt"
f = open(filename, 'w')        
f.writelines(depth_print)
f.close()
   
        
        
        
        
        
    




