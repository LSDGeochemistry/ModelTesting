import numpy as np
import matplotlib
import matplotlib.pyplot as plt

x = np.arange(0,26,1)

full_z = np.zeros_like(x,dtype=float)

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
S_c = 0.65
# soil production
w0 = 0.0002
gamma = 0.5
# Get ekevations
z_0 = 22
full_z[0]=z_0
a=0.15
#
for i in range(1,len(x)):
    full_z[i] = z_0-(a*x[i]*(np.log(x[i])-1))



grad = np.zeros_like(x,dtype=float)
# get the gradients

for i in range(1,len(grad)):
        grad[i] = np.sqrt((full_z[i-1]-full_z[i])**2)



h = np.zeros_like(x,dtype=float)
for i in range(0,len(h)):
    local_curv = ((grad[i]/(1-(grad[i]/S_c)**2))-(grad[i-1]/(1-(grad[i-1]/S_c)**2)))
    dzdt = D*(-(np.sqrt(local_curv**2)))


    h[i] = gamma*np.sqrt(1+grad[i]**2)*np.log(-rho_ratio*(w0/dzdt)*np.sqrt(1+grad[i]**2))

depth = full_z-h
print(grad[40])
print(h[[0,8,16,24,32,40,48]])
print(full_z[[0,8,16,24,32,40,48]])

fig=plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(x,full_z,c='k')
ax.set_xlim(0,max(x))
ax1=ax.twinx()
ax1.plot(x,h)
ax1.set_ylim(0,2.5)
plt.show()
