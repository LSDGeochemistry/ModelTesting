import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from itertools import repeat
#Import the data_
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/steady_state_tests/analytical_linear_test/'
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/production_test/'

print('This is the input file directory: '+DataDirectory)
#Load all the data
print('Load the flowtube data')
ft_out = pd.read_csv(DataDirectory+'ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )
print('Load the eroded particle data')
eroded_bins = pd.read_csv(DataDirectory+'ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
print('Load the particle data')
bins = pd.read_csv(DataDirectory+'p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )


ft_pits = ft_out.s.unique()
ft_pits = np.array(ft_pits)
ft_pits = np.delete(ft_pits, np.where(ft_pits == '-99'))
ft_pits = np.delete(ft_pits, np.where(ft_pits == 's'))
ft_pits = ft_pits.astype(np.float)
# print(ft_pits)
ft_data = ft_out
ft_data = ft_data.drop(ft_data[(ft_data.s == 's') | (ft_data.s == '-99')].index)
ft_data = np.array(ft_data)
ft_data = ft_data.astype(np.float)






timesteps = int(len(ft_data)/len(ft_pits))
pits = int(len(ft_pits))



time_unique = bins.time.unique()
time_unique = np.array(time_unique)
time_unique = time_unique/1000
timelabels = time_unique
bins_unique = bins.bn.unique()
bins_unique = np.array(bins_unique)
bins['time'] = bins['time']/1000
eroded_bins['time'] = eroded_bins['time']/1000
div = max(bins_unique)/max(ft_pits)

# Starting concentration
c_0 = 0
#Production rate at surface (atoms/g/a) 
p = 4.075213




#density of material (g/cm^3)
rho = 1.325
#density of quartz (g/cm^3)
rho_q =2.65
#Decay Constant
gamma = 500*np.power(10.0,-9)
#attenuation lenth (g/cm^2)
l = 160 #from the LSD mixing model
w= 0.006
z_max= 60.108386
# Taken from Foster 2015
z_r = l/rho
z_s =l/rho_q
# start_be_mean = ((p_0/w)*(((rho/rho_q)*z_r*(1-np.exp(-z_max/z_r)))+((np.exp(-z_max/z_r)*z_s)/(1+(gamma*z_s/w)))))/(1+(gamma*z_max*rho_q/(w*rho)))
# F0 mean
p_0 =0.57622337*p
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




start_be_mean = f0+f1+f2+f3
   
    





colors = plt.cm.viridis(np.linspace(0,1,len(time_unique)))

fig = plt.figure(figsize =(16,6))
ax = plt.subplot(1,2,1)
for q in range(0,len(time_unique)):
    i=q*2-1
    i=q
    
    thick = ft_data[i*pits:i*pits+pits][:,5]
    
    for j in range(0,len(bins_unique)//2):
        
        temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['bn'] >= bins_unique[j*2]) & (bins['bn'] <= bins_unique[j*2+1]) & (bins['d_loc'] < thick[j])]
        mean_crn = temp_bins.median().be_conc
        # std_error = temp_bins.std().be_conc
        cb = ax.scatter((bins_unique[j*2+1]/2),mean_crn,color=colors[i],s=10)
        # ax.errorbar((bins_unique[j*2+1]/2),mean_crn,color=colors[i],yerr=std_error)
        cb.set_clim(vmin=0,vmax=max(time_unique))
ax.set_xlim(0,max(bins_unique)/div)
ax.set_ylim(30000,40000)
ax.axhline(y=start_be_mean,color="black",linestyle="--",label='Foster et al, (2015) analytical solution')
ax.legend(loc=4)
ax.set_ylabel(' Mean $^1$$^0$Be Concentration in soil column (atoms g$^-$$^1$)',fontsize=15)
ax.set_title('Linear Sediment Flux Law',fontsize=12)



# Nonlinear Solution
#Import the data_
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/steady_state_tests/analytical_nonlinear_test/'

print('This is the input file directory: '+DataDirectory)
#Load all the data
print('Load the flowtube data')
ft_out = pd.read_csv(DataDirectory+'ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )
print('Load the eroded particle data')
eroded_bins = pd.read_csv(DataDirectory+'ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
print('Load the particle data')
bins = pd.read_csv(DataDirectory+'p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )


# Set up the ds distances

ft_pits = ft_out.s.unique()
ft_pits = np.array(ft_pits)
ft_pits = np.delete(ft_pits, np.where(ft_pits == '-99'))
ft_pits = np.delete(ft_pits, np.where(ft_pits == 's'))
ft_pits = ft_pits.astype(np.float)
# print(ft_pits)
ft_data = ft_out
ft_data = ft_data.drop(ft_data[(ft_data.s == 's') | (ft_data.s == '-99')].index)
ft_data = np.array(ft_data)
ft_data = ft_data.astype(np.float)






timesteps = int(len(ft_data)/len(ft_pits))
pits = int(len(ft_pits))



time_unique = bins.time.unique()
time_unique = np.array(time_unique)
time_unique = time_unique/1000
timelabels = time_unique
bins_unique = bins.bn.unique()
bins_unique = np.array(bins_unique)
bins['time'] = bins['time']/1000
eroded_bins['time'] = eroded_bins['time']/1000
div = max(bins_unique)/max(ft_pits)









colors = plt.cm.viridis(np.linspace(0,1,len(time_unique)))

ax = plt.subplot(1,2,2)
for  q in range(0,len(time_unique)):
    i=q*2-1
    i=q
    thick = ft_data[i*pits:i*pits+pits][:,5]
    
    for j in range(0,len(bins_unique)//2):
        
        temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['bn'] >= bins_unique[j*2]) & (bins['bn'] <= bins_unique[j*2+1]) & (bins['d_loc'] <= thick[j])]
        mean_crn = temp_bins.median().be_conc
        # std_error = temp_bins.std().be_conc
        cb = ax.scatter((bins_unique[j*2+1]/2),mean_crn,color=colors[i],s=10)
        # ax.errorbar((bins_unique[j*2+1]/2),mean_crn,color=colors[i],yerr=std_error)
        cb.set_clim(vmin=0,vmax=max(time_unique))
ax.set_xlim(0,max(bins_unique)/div)
ax.set_ylim(30000,40000)
ax.axhline(y=start_be_mean,color="black",linestyle="--",label='Foster et al, (2015) analytical solution')
ax.legend(loc=4)
ax.set_title('Nonlinear Sediment Flux Law',fontsize=12)








# ax =fig.add_subplot(1,3,3,frameon=False)
# axcb = plt.colorbar(cb)
# axcb.ax.set_ylabel('Time (kiloyears)',fontsize=12)

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.1, 0.02, 0.78])
axcb = plt.colorbar(cb, cax=cbar_ax)
axcb.ax.set_ylabel('Time (kiloyears)',fontsize=12)

ax =fig.add_subplot(1,1,1,frameon=False)
ax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)


ax.set_xlabel('Distance Downslope (m)',fontsize=20)



# plt.savefig(DataDirectory+'/analytical_solutions_median.png', dpi=100, bbox_inches='tight')