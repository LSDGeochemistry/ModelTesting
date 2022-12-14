import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from itertools import repeat

# Starting concentration
c_0 = 0
#Production rate at surface (atoms/g/a) 
# p_0 = 2.41

p = 4.075213





#density of material (g/cm^3)
rho = 1.325
#density of quartz (g/cm^3)
rho_q = 2.65
#Decay Constant
gamma = 500*np.power(10.0,-9)


#attenuation lenth (g/cm^2)
l = 160 #from the LSD mixing model
w= 0.006

# w = 0.01

z_max= 60.108386
# z_max= 35.0
p_0=2.41
z_r = l/rho
z_s =l/rho_q
be_mean = ((p_0/w)*(((rho/rho_q)*z_r*(1-np.exp(-z_max/z_r)))+((np.exp(-z_max/z_r)*z_s)/(1+(gamma*z_s/w)))))/(1+(gamma*z_max*rho_q/(w*rho)))



# F0 mean
p_0 =0.57622337*p
# p_0 =1.62578*p

f0 = ((p_0/w)*(((rho/rho_q)*z_r*(1-np.exp(-z_max/z_r)))+((np.exp(-z_max/z_r)*z_s)/(1+(gamma*z_s/w)))))/(1+(gamma*z_max*rho_q/(w*rho)))
# F1 mean
p_0 = 0.012937671*p
l =1459.767
z_r = l/rho
z_s =l/rho_q
f1 = ((p_0/w)*(((rho/rho_q)*z_r*(1-np.exp(-z_max/z_r)))+((np.exp(-z_max/z_r)*z_s)/(1+(gamma*z_s/w)))))/(1+(gamma*z_max*rho_q/(w*rho)))
# F2 mean
p_0 = 0.002505*p
l=11039.24
z_r = l/rho
z_s =l/rho_q
f2 = ((p_0/w)*(((rho/rho_q)*z_r*(1-np.exp(-z_max/z_r)))+((np.exp(-z_max/z_r)*z_s)/(1+(gamma*z_s/w)))))/(1+(gamma*z_max*rho_q/(w*rho)))
# f3 mean
p_0 =0*p
z_r = l/rho
z_s =l/rho_q
f3 = ((p_0/w)*(((rho/rho_q)*z_r*(1-np.exp(-z_max/z_r)))+((np.exp(-z_max/z_r)*z_s)/(1+(gamma*z_s/w)))))/(1+(gamma*z_max*rho_q/(w*rho)))



be_mean = f0+f1+f2
# print(be_mean)
print(f0)
print(f1)
print(f2)




# saprolite values
h=60.103
p = 4.075213
p_0 =0.57622337*p
l=160
z_r = l/rho
z_s = l/rho_q
be_s_neut = (z_s*(p_0*np.exp(-h/z_r)))/(w+gamma*z_s)


p_0 = 0.002505*p
l=11039.24
z_r = l/rho
z_s = l/rho_q
be_s_muon = (z_s*(p_0*np.exp(-h/z_r)))/(w+gamma*z_s)


p_0 = 0.012937671*p
l =1459.767
z_r = l/rho
z_s = l/rho_q
be_s_oth = (z_s*(p_0*np.exp(-h/z_r)))/(w+gamma*z_s)
print(be_s_neut)
print(be_s_oth)
print(be_s_muon)


be_tot = be_s_neut+be_s_oth+be_s_muon

# w=0.01
# rho_q = 2.65
# rho = 1.325
# h=np.arange(0,400,1)
# p = 4.075213
# p_0 =0.57622337*p
# l=160
# z_r = l/rho
# z_s = l/rho_q
# be_s_neut = (z_s*(p_0*np.exp(-h/z_r)))/(w+gamma*z_s)

# p_0 = 0.002505*p
# l=11039.24
# z_r = l/rho
# z_s = l/rho_q
# be_s_muon = (z_s*(p_0*np.exp(-h/z_r)))/(w+gamma*z_s)


# p_0 = 0.012937671*p
# l =1459.767
# z_r = l/rho
# z_s = l/rho_q
# be_s_oth = (z_s*(p_0*np.exp(-h/z_r)))/(w+gamma*z_s)



# be_tot1 = be_s_neut+be_s_oth+be_s_muon

# print(be_tot1[35])
# print(be_tot[35])
# print(be_mean)
# fig = plt.figure()
# ax = plt.subplot(1,1,1)
# ax.scatter(be_mean,z_max)
# plt.gca().invert_yaxis()


# plt.show()

