import numpy as np
import matplotlib
import matplotlib.pyplot as plt
x_dist = 1.0
x = np.arange(0,43,x_dist)

# constants
c = 25
# uplift
C_0 = 0.0001
# Sediment transport coefficient
D = 0.002
# density
rho_r = 2650
rho_s = 1325
rho_ratio = rho_r/rho_s
# erosion
E = 0.0001
# soil production
w0 = 0.0002
gamma = 2.0
gamma_i = 1/gamma
# Critical slope
S_c = 0.65
# Get elevations Roering
beta = rho_ratio*C_0
first_part = - S_c*S_c*0.5/beta
second_part = np.sqrt( D*D + (2*beta*x/S_c)*(2*beta*x/S_c) )
third_part = D*np.log(S_c*(second_part+D)*0.5/beta)
full_z_r = first_part*(second_part-third_part)+c

min_val = full_z_r[len(x)-1]
new_z_r = full_z_r-min_val

# Get elevations Pelletier
full_z_p = np.zeros_like(x,dtype=float)
z_0 = 22
full_z_p[0]=z_0
a=0.15
#
for i in range(1,len(x)):
    full_z_p[i] = z_0-(a*x[i]*(np.log(x[i])-1))
min_val = full_z_p[len(x)-1]
full_z_p = full_z_p-min_val

# print(new_z)
grad_r = np.zeros_like(x,dtype=float)
grad_p = np.zeros_like(x,dtype=float)

# get the gradients

for i in range(1,len(grad_r)-1):
        grad_r[i] = 0.5*((new_z_r[i-1]-new_z_r[i])/x_dist+(new_z_r[i]-new_z_r[i+1])/x_dist)
        grad_p[i] = np.sqrt(((full_z_p[i-1]-full_z_p[i])/x_dist)**2)

# convert to degrees
grad_d_r = (np.rad2deg(np.arctan(grad_r)))
# Get the soil thickness for Roering solution
h_r = np.zeros_like(x,dtype=float)
for i in range(0,len(h_r)):
    h_r[i] = (-np.log((E/w0)*np.cos(np.deg2rad(grad_d_r[i]))))/(gamma*np.cos(np.deg2rad(grad_d_r[i])))
# Get the soil thickness for Pelletier solution
h_p = np.zeros_like(x,dtype=float)
for i in range(0,len(h_p)):
    local_curv = np.sqrt(((grad_p[i]/(1-(grad_p[i]/S_c)**2))-(grad_p[i-1]/(1-(grad_p[i-1]/S_c)**2)))**2)
    dzdt = D*(-(np.sqrt(local_curv**2)))


    h_p[i] = gamma_i*np.sqrt(1+grad_p[i]**2)*np.log(-rho_ratio*(w0/dzdt)*np.sqrt(1+grad_p[i]**2))


# print(h)
depth_r = new_z_r-h_r
depth_p = full_z_p-h_p

fig=plt.figure()

# plot Roering
ax = fig.add_subplot(2,1,1)
ax.plot(x,new_z_r,c='k')
ax.set_xlim(0,max(x)-1)
ax1=ax.twinx()
ax1.plot(x,h_r)
ax1.set_ylim(0,2.5)
# plot Pelletier
ax = fig.add_subplot(2,1,2)
ax.plot(x,full_z_p,c='k')
ax.set_xlim(0,max(x)-1)
ax1=ax.twinx()
ax1.plot(x,h_p)
ax1.set_ylim(0,2.5)

# ax = fig.add_subplot(1,1,1,frame_on=False,visible=False)
# ax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
#
# ax.set_xlabel('Distance (m)')
# ax.set_ylabel('Elevation (m)')
# ax1=ax.twinx()
# ax1.set_ylabel('Soil Depth (m)')
# ax1.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
print(h_r[[0,6,12,18,24,30,36,42]])
print(full_z_p[[0,6,12,18,24,30,36,42]])
plt.show()
