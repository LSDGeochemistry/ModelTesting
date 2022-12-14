#This Script produces graphs from a succesful mixing column run

#IMport the pacakges
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from itertools import repeat
#Import the data_
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/changing_base_level/0_1mm_nonlinear/0mm_mixing_full_cosmo_longer/'
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/sensitivity_tests/analytical_linear_test_upgraded_mm/'
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/pomd/pomd_test_run/'
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/feather_runs/brc/linear/'
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/test_catena/'
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/steady_state_tests/analytical_linear_test_neutron_insert/'


print('This is the input file directory: '+DataDirectory)
#Load all the data
print('Load the flowtube data')
ft_out = pd.read_csv(DataDirectory+'ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )
print('Load the eroded particle data')
eroded_bins = pd.read_csv(DataDirectory+'ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
print('Load the particle data')
bins = pd.read_csv(DataDirectory+'p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )

# General Profiles
print('Creating the profile figures...')
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


# Hillslope profile
fig = plt.figure()
ax = plt.subplot(1,1,1)
# Set up the plots based on times
for i in range(0,timesteps):
    ds_dist = ft_data[i*pits:i*pits+pits][:,0]
    elev = ft_data[i*pits:i*pits+pits][:,3]
    elev = elev-min(elev)
    cb = ax.scatter(ds_dist,elev,s=2,color=colors[i])
    cb.set_clim(vmin=0,vmax=max(time_unique))
ax.set_ylabel('Elevation (m)',fontsize=16)
ax.set_xlabel('Distance Downslope (m)',fontsize=16)
axcb = plt.colorbar(cb)
axcb.ax.set_ylabel('Time (kiloyears)',fontsize=12)

plt.tight_layout()
plt.savefig(DataDirectory+'/hillslope_profile_with_time.png', dpi=100, bbox_inches='tight')

fig = plt.figure()
ax = plt.subplot(1,1,1)
# Soil Depth profiles
for i in range(0,timesteps):
    ds_dist = ft_data[i*pits:i*pits+pits][:,0]
    thick = ft_data[i*pits:i*pits+pits][:,5]
    cb = ax.scatter(ds_dist,thick,s=2,color=colors[i])
    cb.set_clim(vmin=0,vmax=max(time_unique))
ax.set_ylabel('Soil Thickness (m)',fontsize=16)
ax.set_xlabel('Distance Downslope (m)',fontsize=16)
axcb = plt.colorbar(cb)
axcb.ax.set_ylabel('Time (kiloyears)',fontsize=12)
plt.tight_layout()
plt.savefig(DataDirectory+'/soil_thickness_with_time.png', dpi=100, bbox_inches='tight')


# # #Fluxes
# print('Creating the flux figures...')
# #Plot the lower flux boxplot
# fig = plt.figure()
# ax = plt.subplot(1,1,1)
# plot_bins = [[] for i in (time_unique)]
# for i in range(0,len(time_unique)):
#     temp_bins=eroded_bins[(eroded_bins['time'] == time_unique[i]) & (eroded_bins['bn'] == eroded_bins.bn.max())]
#     plot_bins[i] = np.append(plot_bins[i], [temp_bins['be_conc']])

# ax.boxplot(plot_bins,showfliers=False,labels=timelabels)
# ax.set_ylabel('$^1$$^0$Be Concentration (atoms g$^-$$^1$)',fontsize=20)
# ax.set_xlabel('Age (kiloyears)',fontsize=20)
# plt.tight_layout()
# plt.savefig(DataDirectory+'hillslope_crn_conc_flux_output', dpi=100, bbox_inches='tight')



# fig = plt.figure()
# ax = plt.subplot(1,1,1)

# plot_bins = [[] for i in (time_unique)]
# for i in range(0,len(time_unique)):
#     temp_bins=eroded_bins[(eroded_bins['time'] == time_unique[i]) & (eroded_bins['bn'] == eroded_bins.bn.max())]
#     plot_bins[i] = np.append(plot_bins[i], [temp_bins['be_conc']])

# ax.violinplot(plot_bins,showextrema=False,showmedians=True,positions=timelabels,widths=0.5*timelabels[0])
# ax.set_ylabel('$^1$$^0$Be Concentration (atoms g$^-$$^1$)',fontsize=20)
# ax.set_xlabel('Age (kiloyears)',fontsize=20)
# plt.tight_layout()
# plt.savefig(DataDirectory+'hillslope_crn_conc_flux_output_violin', dpi=100, bbox_inches='tight')




#CRN Depth Profiles
print('Creating the depth profiles figures...')
#Hillslope CRN figure
fig = plt.figure()
ax = plt.subplot(1,1,1)
for i in range(0,len(time_unique)):
    thick = ft_data[i*pits:i*pits+pits][:,5]
    # thick = [x for item in thick for x in repeat(item,2)]
    for j in range(0,len(bins_unique)//2):
        
        # temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['bn'] == bins_unique[j]) & (bins['d_loc'] <= thick[j])]
        temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['bn'] >= bins_unique[j*2]) & (bins['bn'] <= bins_unique[j*2+1]) & (bins['d_loc'] < thick[j])]
        mean_crn = temp_bins.mean().be_conc
        # cb = ax.scatter((bins_unique[j]/div),mean_crn,color=colors[i],s=10)
        cb = ax.scatter((bins_unique[j*2+1]/2),mean_crn,color=colors[i],s=10)

        cb.set_clim(vmin=0,vmax=max(time_unique))
ax.set_xlim(0,max(bins_unique)/div)
axcb = plt.colorbar(cb)
axcb.ax.set_ylabel('Time (kiloyears)',fontsize=12)
ax.set_ylabel(' Mean $^1$$^0$Be Concentration in soil_column (atoms g$^-$$^1$)',fontsize=15)
ax.set_xlabel('Distance Downslope (m)',fontsize=20)


# Cosmo

# Starting concentration
c_0 = 0
#Production rate at surface (atoms/g/a) 
# p_0 = 2.35
p_0 = 2.41




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
start_be_mean = ((p_0/w)*(((rho/rho_q)*z_r*(1-np.exp(-z_max/z_r)))+((np.exp(-z_max/z_r)*z_s)/(1+(gamma*z_s/w)))))/(1+(gamma*z_max*rho_q/(w*rho)))
z_max = 35.14
w=0.006    
    
end_be_mean = ((p_0/w)*(((rho/rho_q)*z_r*(1-np.exp(-z_max/z_r)))+((np.exp(-z_max/z_r)*z_s)/(1+(gamma*z_s/w)))))/(1+(gamma*z_max*rho_q/(w*rho)))

ax.axhline(y=start_be_mean,color="black",linestyle="--")
ax.axhline(y=end_be_mean,color="black",linestyle="--")
ax.axhline(y=33061,color="black",linestyle="--")


plt.tight_layout()
plt.savefig(DataDirectory+'crn_hillsope_profile_with_time_soil_column', dpi=100, bbox_inches='tight')



# fig = plt.figure()
# ax = plt.subplot(1,1,1)
# for i in range(0,len(time_unique)):
 
#     for j in range(0,len(bins_unique)):
        
#         temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['bn'] == bins_unique[j]) & (bins['d_loc'] <= 0.1)]
#         mean_crn = temp_bins.mean().be_conc
#         cb = ax.scatter((bins_unique[j]/div),mean_crn,color=colors[i],s=10)
#         cb.set_clim(vmin=0,vmax=max(time_unique))
# ax.set_xlim(0,max(bins_unique)/div)
# axcb = plt.colorbar(cb)
# axcb.ax.set_ylabel('Time (kiloyears)',fontsize=12)
# ax.set_ylabel(' Mean $^1$$^0$Be Concentration in top 0.1m (atoms g$^-$$^1$)',fontsize=15)
# ax.set_xlabel('Distance Downslope (m)',fontsize=20)
# plt.tight_layout()
# plt.savefig(DataDirectory+'crn_hillsope_profile_with_time_top_cms', dpi=100, bbox_inches='tight')
#Crn depth profiles
# Set up the bin intervals
depth_bins =[[0,0.1],[0.1,0.2],[0.2,0.3],[0.3,0.4],[0.4,0.5],[0.5,0.6],[0.6,0.7],[0.7,0.8],[0.8,0.9],[0.9,1.0]]
ft_pits =[min(ft_pits),max(ft_pits)*0.25,max(ft_pits)*0.5,max(ft_pits)*0.75,max(ft_pits)]

# Set up the plots based on times
for i in range(0,len(time_unique)):
    fig = plt.figure(figsize =(18,6))
    t = time_unique[i]*1000
    # print(t)
    # Set up the different pits and plot
    for j in range(0,len(ft_pits)):
        upp = ft_pits[j]+0.5
        low = ft_pits[j]-0.5
        temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['s_loc'] <= upp) & (bins['s_loc'] >= low)]
        # Set up the plot
        ax = plt.subplot(1,len(ft_pits),j+1)
        ax.scatter(temp_bins.be_conc,temp_bins.d_loc,c='0.6',s=0.05)

        # print(c_z)
        # ax.plot(c_z,z/100,c='k', label = 'Lal and Chen (2005)')
        # Now do the depth n_bins
        for k in range(0,len(depth_bins)-1):
            temp = temp_bins[(temp_bins.d_loc >= depth_bins[k][0]) & (temp_bins.d_loc <= depth_bins[k][1])]
            #Find the mean values of each bi
            mean_d = temp.mean().d_loc

            mean_be = temp.mean().be_conc
            be_std = temp.std().be_conc
            d_std = temp.std().d_loc
            
            ax.errorbar(mean_be,mean_d,xerr=be_std,fmt='none',c='k',ls='--')
            ax.scatter(mean_be,mean_d,s=20,c='k')





            
            
            plt.gca().invert_yaxis()
            ax.set_title('Pit '+str(j+1)+' ('+str(ft_pits[j])+'m downslope)',fontsize=12)
            if j > 0:
                ax.set_yticklabels([])

    
    

    ax =fig.add_subplot(1,1,1,frameon=False)
    ax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    ax.set_ylabel('Depth (m)',fontsize=18)
    
    ax.set_xlabel('$^1$$^0$Be Concentration atoms g$^-$$^1$',fontsize=18)


    plt.tight_layout()
    plt.savefig(DataDirectory+'/hillslope_crn_conc_bins_depth_profile_binned_'+str(int(time_unique[i]))+'.png', dpi=100, bbox_inches='tight')

# Turnover time comparison

# Read in data
# base level file
# bl_in = pd.read_csv(DataDirectory+'base_level_hist.param',header=None ,sep=" ")

# bl_counter = 0
# bl_age = bl_in[bl_counter][0]
# bl_old_c = 0
# bl_counter = 0

# # original elev data
# prof_in = pd.read_csv(DataDirectory+'profile.sm',header=None,delim_whitespace=True)
# # erosion rate file
# er_in = pd.read_csv(DataDirectory+'erate_hist.param',header=None, sep=" ")
# erosion_counter = 0
# erosion_age = er_in[erosion_counter][0]
# erosion = er_in[erosion_counter+1][0]

# # sed trans file
# sed_trans_in = pd.read_csv(DataDirectory+'sed_trans_param.stparam',header=None, sep=" ")
# K = sed_trans_in[1][2]
# # model run
# model_run_in = pd.read_csv(DataDirectory+'model_run.param',header=None, sep=" ")
# final_node = model_run_in[1][17]



# # Set up the plots based on times
# for i in range(0,timesteps):
#     fig = plt.figure()
#     ax = plt.subplot(1,1,1)

#     if time_unique[i]*1000 > erosion_age:
#         erosion_counter = erosion_counter+2
#     if time_unique[i]*1000 > bl_age:
#         diff = time_unique[i]*1000-bl_age
#         bl_old_c = bl_counter
#         bl_counter = bl_counter+2 
#     else:
#         diff = 0  
#     final_node = final_node-((time_unique[i]-(time_unique[0]*i))*1000-diff)*bl_in[bl_old_c+1][0]-(diff*bl_in[bl_counter+1][0])
#     final_node = np.around(final_node,3)

    
#     bl_old_c = bl_counter
#     bl_age = bl_in[bl_counter][0]
    
    

#     ds_dist = ft_data[i*pits:i*pits+pits][:,0]
#     elev_old = prof_in[3][:]-min(prof_in[3][:])+1000
    
#     elev = ft_data[i*pits:i*pits+pits][:,3]
#     if i == 0:
#         lowering = (elev_old-elev)/(time_unique[0]*1000)
        
#     else:
#         lowering = (ft_data[(i-1)*pits:(i-1)*pits+pits][:,3]-elev)/((time_unique[i]-time_unique[i-1])*1000)

#     thick = ft_data[i*pits:i*pits+pits][:,5]
    
#     # width = ft_data[i*pits:i*pits+pits][:,1]
#     # slope = np.zeros(len(elev))
#     # flux = np.zeros(len(elev))
#     # t = np.zeros(len(elev))
#     # for j in range(0,len(elev)-1):
#     #     slope[j] = (elev[j]-elev[j+1])/(ds_dist[j+1]-ds_dist[j])

#     # slope[len(slope)-1] = (elev[len(slope)-1]-final_node)/(ds_dist[len(slope)-1]-ds_dist[len(slope)-2])
    
#     # flux[0]= K*thick[0]*width[0]*slope[0]

#     # for j in range(1,len(flux)):
#     #     flux[j] = (K*thick[j]*width[j]*slope[j])-(K*thick[j-1]*width[j-1]*slope[j-1])
    
#     # for j in range(0,len(flux)):
#     # t[j] = thick[j]/(flux[j]+erosion)

#     t = thick/((lowering+erosion)*(sed_trans_in[1][1]/sed_trans_in[1][0]))
    

#     cb = ax.scatter(ds_dist,t,s=3)
#     for j in range(0,len(ds_dist)):
#         temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['bn'] >= bins_unique[j*2]) & (bins['bn'] <= bins_unique[j*2+1]) & (bins['d_loc'] <= thick[i])]
#         mean_crn = temp_bins.mean().page
#         cb = ax.scatter(ds_dist[j],mean_crn,s=3,marker='X',c='k')
   
#     ax.set_ylabel('Turnover time (yrs)',fontsize=16)
#     ax.set_xlabel('Distance Downslope (m)',fontsize=16)
    

#     plt.tight_layout()
#     plt.savefig(DataDirectory+'/hillslope_turnover_vs_mean_age_new'+str(int(time_unique[i]))+'.png', dpi=100, bbox_inches='tight')
 