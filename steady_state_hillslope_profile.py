import numpy as np
import matplotlib
import matplotlib.pyplot as plt

x = np.arange(0,26,1)

# constants
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
gamm_i = 1/gamma
# Critical slope
S_c = 0.65
# Get elevations Roering
beta = rho_ratio*C_0
first_part = -beta/(2*D)
second_part = np.multiply(x,x)
full_z_r = first_part*second_part

min_val = full_z_r[max(x)]
new_z_r = full_z_r-min_val

# Get elevations Pelletier
full_z = np.zeros_like(x,dtype=float)
z_0 = 22
full_z_p[0]=z_0
a=0.15
#
for i in range(1,len(x)):
    full_z_p[i] = z_0-(a*x[i]*(np.log(x[i])-1))


# print(new_z)
grad_r = np.zeros_like(x,dtype=float)
grad_p = np.zeros_like(x,dtype=float)
# get the gradients

for i in range(1,len(grad)-1):
        grad_r[i] = 0.5*((new_z_r[i-1]-new_z_r[i])+(new_z_r[i]-new_z_r[i+1]))
        grad_p[i] = 0.5*((new_z_p[i-1]-new_z_p[i])+(new_z_p[i]-new_z_p[i+1]))

# convert to degrees
grad_d_r = (np.rad2deg(np.arctan(grad_r)))
# Get the soil thickness for Roering solution
h_r = np.zeros_like(x,dtype=float)
for i in range(0,len(h)):
    h_r[i] = (-np.log((E/w0)*np.cos(np.deg2rad(grad_d_r[i]))))/(gamma*np.cos(np.deg2rad(grad_d_r[i])))
# Get the soil thickness for Pelletier solution
h_p = np.zeros_like(x,dtype=float)
for i in range(0,len(h)):
    local_curv = ((grad_p[i]/(1-(grad[i]_p/S_c)**2))-(grad_p[i-1]/(1-(grad_p[i-1]/S_c)**2)))
    dzdt = D*(-(np.sqrt(local_curv**2)))


    h_p[i] = gamma*np.sqrt(1+grad_p[i]**2)*np.log(-rho_ratio*(w0/dzdt)*np.sqrt(1+grad_p[i]**2))


# print(h)
depth_r = new_z_r-h_r
depth_p = full_z_p-h_p

fig=plt.figure()
# plot Roering
ax = fig.add_subplot(2,1,1)
ax.plot(x,full_z_r,c='k')
ax.set_xlim(0,max(x))
ax1=ax.twinx()
ax1.plot(x,h_r)
ax1.set_ylim(0,2.5)
# plot Pelletier
fig=plt.figure()
ax = fig.add_subplot(2,1,2)
ax.plot(x,full_z_p,c='k')
ax.set_xlim(0,max(x))
ax1=ax.twinx()
ax1.plot(x,h_p)
ax1.set_ylim(0,2.5)

plt.show()
