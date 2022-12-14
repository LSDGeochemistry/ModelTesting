import numpy as np
import matplotlib
import matplotlib.pyplot as plt

x = np.arange(0,31+1/2,1/2)

# constants
# uplift
C_0 = 0.0001
# Sediment transport coefficient
D = 0.005
# density
rho_r = 2650
rho_s = 1325
rho_ratio = rho_r/rho_s
# erosion
E = 0.0001
# soil production
w0 = 0.0002
gamma = 2.0
# Get ekevations
beta = rho_ratio*C_0
first_part = -beta/(2*D)
second_part = np.multiply(x,x)
full_z = first_part*second_part

min_val = min(full_z)
new_z = full_z-min_val
# print(new_z)
grad = np.zeros_like(x,dtype=float)
# get the gradients

for i in range(1,len(grad)-1):
        grad[i] = 0.5*((new_z[i-1]-new_z[i])+(new_z[i]-new_z[i+1]))
# convert to degrees

grad_d = np.arctan(grad)

h = np.zeros_like(x,dtype=float)
for i in range(0,len(h)):
    h[i] = (-np.log((E/w0)*np.cos((grad_d[i]))))/(gamma*np.cos((grad_d[i])))
# h_test = np.zeros_like(x,dtype=float)
# for i in range(0,len(h)-1):
#     h_test[i] = (((gamma)/np.cos(grad_d[i]))*np.log(rho_ratio*(w0/(D*np.cos(grad_d[i])))*(1/-(grad[i]-grad[i+1]))))

# print(h)
depth = new_z-h

# print(new_z)


# fig=plt.figure()
# ax = fig.add_subplot(1,1,1)
# ax.plot(x,new_z,c='k')
# ax.plot(x,depth)
# plt.show()

# Create the output data
width = np.ones_like(x,dtype = int)
area = width*(1/2)
ft_param = np.vstack((x,width,area,new_z,h)).T
# Create the dataframe to output
np.savetxt("flowtube_details_high_k.csv", ft_param, delimiter=" ",header='ds_dist,area,A_pol,meas_elev,interp_h')

