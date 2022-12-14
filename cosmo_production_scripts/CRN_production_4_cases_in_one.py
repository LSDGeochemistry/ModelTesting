

#Cosmo concentraion data with depth based on equation 20 in Niedermann, 2002 paper

import numpy as np
import matplotlib.pyplot as plt
#Time (a)
t = 10000
# Starting concentration
c_0 = 0
#Production rate at surface (atoms/g/a) (taken from Table 6)
# p_0 = 4.075
p_0 = 2.35

#Depth of profile (cm)
d = 100
#Depth profile for testing
z = np.arange(0,d,0.001)
#density of material (g/cm^3)
rho = 1.325
#density of quartz (g/cm^3)
rho_q =2.65
#Decay Constant
gamma = 500*np.power(10.0,-9)
#attenuation lenth (g/cm^2)
l = 160 #from the LSD mixing model
#Production rate at different depth each year
p_z = p_0*np.exp(-rho*z/l)
#Production for x number of years
p_z_t = p_z*t
#print p_z_t
#Load the mixing model output
data2 = np.genfromtxt('/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/Model_testing/run1/p_trans_out.pout', delimiter=' ',skip_header=0, names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','c_conc','ne_conc'])
be_conc =data2['be_conc']
d_loc =data2['d_loc']*100

fig = plt.figure()
ax = fig.add_subplot(2,2,1)
plt.tick_params(axis='both', which='major', labelsize=8)
ax.scatter(be_conc,d_loc,color='0.5',s= 0.5, label = 'Mixing Model')
ax.plot(p_z_t,z,c='k',label = 'Lal and Chen (2005)')
ax.title.set_text('No erosion, No mixing')

ax.set_ylim(0,100)
ax.set_xlim(0)
plt.gca().invert_yaxis()
plt.legend(loc=2,fontsize='6')
# plt.savefig('crn_no_erosion_no_mixing.png', dpi=800, bbox_inches='tight')


#Cosmo concentraion data wit hdepth based on equation A" in Brown ert al 1995 paper


#Load the mixing model output
data2 = np.genfromtxt('/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/Model_testing/run2/p_trans_out.pout', delimiter=' ',skip_header=0, names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','c_conc','ne_conc'])
be_conc =data2['be_conc']
d_loc =data2['d_loc']*100

#Depth of profile (cm)
d = 100
#Depth profile for testing
z = np.arange(0,d,0.01)





#Assuming full mixing across the column find the average production rate
#From Riebe and Granger (2014) Equation 16
# p_ave = (p_0/(d*l**-1))*(1-np.exp(-d*l**-1))
p_ave =(p_0*l)/(rho*d)*(1-np.exp(-rho*d/l))

p = p_ave*t
mixed = (p-(p*gamma))

ax = fig.add_subplot(2,2,2)


plt.tick_params(axis='both', which='major', labelsize=8)
ax.scatter(be_conc,d_loc,color='0.5',s= 0.5, label = 'Mixing Model')
plt.axvline(mixed ,c='k',label='Granger and Riebe (2014)')
ax.set_ylim(0,100)
ax.set_xlim(0)
ax.title.set_text('No erosion, Mixing')
plt.gca().invert_yaxis()
plt.legend(loc=2,fontsize='6')



#Method from Lal and Chen 2005 (time in years rather than seconds)
data2 = np.genfromtxt('/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/Model_testing/run3/p_trans_out.pout', delimiter=' ',skip_header=0, names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','c_conc','ne_conc'])
be_conc =data2['be_conc']
d_loc =data2['d_loc']*100
z = np.arange(0,100,0.001)
#Erosion rate (cm/yr)
e = 0.01



c_z = c_0*np.exp(-gamma*t)+((p_0*np.exp(-rho*z/l))/(gamma+rho*e/l))*(1-np.exp(-t*(gamma+rho*e/l)))


ax = fig.add_subplot(2,2,3)

ax.set_ylim(0,100)
plt.tick_params(axis='both', which='major', labelsize=8)
ax.scatter(be_conc,d_loc,color='0.5',s= 0.5, label = 'Mixing Model')
ax.plot(c_z,z,c='k', label = 'Lal and Chen (2005)')
ax.title.set_text('Erosion, No Mixing')
ax.set_xlim(0)
plt.gca().invert_yaxis()
plt.legend(loc=2,fontsize='6')

data2 = np.genfromtxt('/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/Model_testing/run4/p_trans_out.pout', delimiter=' ',skip_header=0, names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','c_conc','ne_conc'])

be_conc =data2['be_conc']
d_loc =data2['d_loc']*100
#Method from Lal and Chen 2005 (time in years rather than seconds)
z = 100
d = 100
#Simplified for equation (13) below
#overlying mass (g/cm^2)
x = z*rho
#Radioactive decay constant (a)
lm = gamma
p = p_0
#Erosion rate (g/cm^2/a)
e = 0.01*rho
#Bioturbation depth (cm)
b = d
#Part of profile affected by Bioturbation
x_b = d


#Brown method for bioturbated soil
N = (((l*np.exp(-x_b*l**-1))/(l-x_b))*((p/(e*l**-1+lm))*(1-np.exp(-t*(e*l**-1+lm))))+(1-(l*np.exp(-x_b*l**-1))/(l-x_b))*((p/(e*l**-1+lm*x_b*l**-1))*(1-np.exp(-t*(e*x_b**-1+lm)))))
print(N)
#Changes it so the negative concentration equal 0 instead
# Riebe and Granger method
# p_ave =(p_0*l)/(rho*d)*(1-np.exp(-rho*d/l))
# N_brac = (p_0*l*tau)/(rho*d)*(1-np.exp(-rho*d/l))*(1-np.exp(-t/tau))
# print(N_brac)
# N_sap = p*np.exp(-rho*d/l)*l/e
# print(N_sap)
# p_tot = t*(p_ave-(N_brac/tau)-(N_brac*e/rho*d)+(N_sap*e/rho*d))

ax = fig.add_subplot(2,2,4)



ax.set_ylim(0,100)
plt.tick_params(axis='both', which='major', labelsize=8)
ax.scatter(be_conc,d_loc,color='0.5',s= 0.5, label = 'Mixing Model')
plt.axvline(N,c='k',label='Brown et al, (1995)')
ax.title.set_text('Erosion, Mixing')
# ax.plot(c_z,z,c='k',label = 'Lal and Chen Analytical Model')
plt.gca().invert_yaxis()
plt.legend(loc=2,fontsize='6')
ax.set_xlim(0)

ax =fig.add_subplot(1,1,1,frameon=False)
ax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
ax.set_ylabel('Depth (m)',fontsize=18)
    
ax.set_xlabel('$^1$$^0$Be Concentration atoms g$^-$$^1$',fontsize=18)

plt.tight_layout()
plt.savefig('Cosmo_testing_4_in_1.png', dpi=100, bbox_inches='tight')
plt.show()
