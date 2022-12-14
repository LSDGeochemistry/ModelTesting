import numpy as np
import matplotlib
import matplotlib.pyplot as plt

x = np.arange(0,25,1)

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
# Critical slope
S_c = 1.0
# soil production
w0 = 0.0002
gamma = 2.0
# Get ekevations
beta = rho_ratio*C_0
first_part = - S_c*S_c*0.5/beta
second_part = np.sqrt( D*D + (2*beta*x/S_c)*(2*beta*x/S_c) )
third_part = D*np.log(S_c*(second_part+D)*0.5/beta)
full_z = first_part*(second_part-third_part)+c

min_val = full_z[max(x)]
new_z = full_z-min_val
# print(new_z)
grad = np.zeros_like(x,dtype=float)
# get the gradients

for i in range(1,len(grad)):
        grad[i] = new_z[i-1]-new_z[i]
# convert to degrees

grad_d = (np.rad2deg(np.arctan(grad)))
print(grad)
h = np.zeros_like(x,dtype=float)
for i in range(0,len(h)):
    h[i] = (-np.log((E/w0)*np.cos(np.deg2rad(grad_d[i]))))/(gamma*np.cos(np.deg2rad(grad_d[i])))

h_pel = np.zeros_like(x,dtype=float)
for i in range(0,len(h_pel)):
    local_curv = ((grad[i]/(1-(grad[i]/S_c)**2))-(grad[i-1]/(1-(grad[i-1]/S_c)**2)))
    dzdt = D*(-(np.sqrt(local_curv**2)))


    h_pel[i] = (1/gamma)*np.sqrt(1+grad[i]**2)*np.log(-rho_ratio*(w0/dzdt)*np.sqrt(1+grad[i]**2))# print(h)

depth = new_z-h
print(new_z[[0,4,8,12,16,20,24]])
print(h[[0,4,8,12,16,20,24]])
print(h_pel[[0,4,8,12,16,20,24]])
fig=plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(x,new_z,c='k')
ax.set_xlim(0,max(x))
ax1=ax.twinx()
ax1.plot(x,h_pel)
ax1.set_ylim(0,2.5)
plt.show()
