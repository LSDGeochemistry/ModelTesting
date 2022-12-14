#IMport the pacakges
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from itertools import repeat
#Import the data_
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/changing_base_level/0_1mm_linear/0mm_mixing/'
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/steady_state_tests/analytical_linear_test/'
print('This is the input file directory: '+DataDirectory)
#Load all the data
print('Load the flowtube data')
ft_out = pd.read_csv(DataDirectory+'ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )
print('Load the eroded particle data')
eroded_bins = pd.read_csv(DataDirectory+'ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','c_conc','ne_conc'] )
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


#CRN Depth Profiles
print('Creating the depth profiles figures...')
#Hillslope CRN figure
fig = plt.figure()
ax = plt.subplot(1,1,1)
for i in range(0,len(time_unique)):
    thick = ft_data[i*pits:i*pits+pits][:,5]
    thick = [x for item in thick for x in repeat(item,2)]
    for j in range(0,len(bins_unique)):
        
        temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['bn'] == bins_unique[j]) & (bins['d_loc'] <= thick[j])]
        # temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['bn'] == bins_unique[j]) & (bins['d_loc'] <= 0.01)]
        mean_crn = temp_bins.mean().c_conc
        cb = ax.scatter((bins_unique[j]/div),mean_crn,color=colors[i],s=10)
        cb.set_clim(vmin=0,vmax=max(time_unique))
ax.set_xlim(0,max(bins_unique)/div)
axcb = plt.colorbar(cb)
axcb.ax.set_ylabel('Time (kiloyears)',fontsize=12)
ax.set_ylabel(' Mean $^1$$^4$C Concentration in soil_column (atoms g$^-$$^1$)',fontsize=15)
ax.set_xlabel('Distance Downslope (m)',fontsize=20)
plt.tight_layout()
plt.savefig(DataDirectory+'carbon14_hillsope_profile_with_time_soil_column', dpi=100, bbox_inches='tight')

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
        ax.scatter(temp_bins.c_conc,temp_bins.d_loc,c='0.6',s=0.05)

        # print(c_z)
        # ax.plot(c_z,z/100,c='k', label = 'Lal and Chen (2005)')
        # Now do the depth n_bins
        for k in range(0,len(depth_bins)-1):
            temp = temp_bins[(temp_bins.d_loc >= depth_bins[k][0]) & (temp_bins.d_loc <= depth_bins[k][1])]
            #Find the mean values of each bi
            mean_d = temp.mean().d_loc

            mean_be = temp.mean().c_conc
            be_std = temp.std().c_conc
            d_std = temp.std().d_loc
            
            ax.errorbar(mean_be,mean_d,xerr=be_std,fmt='none',c='k',ls='--')
            ax.scatter(mean_be,mean_d,s=20,c='k')





            ax.set_ylim(0,1.0)
            
            plt.gca().invert_yaxis()
            ax.set_title('Pit '+str(j+1)+' ('+str(ft_pits[j])+'m downslope)',fontsize=12)
            if j > 0:
                ax.set_yticklabels([])

    
    

    ax =fig.add_subplot(1,1,1,frameon=False)
    ax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    ax.set_ylabel('Depth (m)',fontsize=18)
    
    ax.set_xlabel('$^1$$^4$C Concentration atoms g$^-$$^1$',fontsize=18)


    plt.tight_layout()
    plt.savefig(DataDirectory+'/hillslope_carbon14_conc_bins_depth_profile_binned_'+str(int(time_unique[i]))+'.png', dpi=100, bbox_inches='tight')

# #Fluxes
print('Creating the flux figures...')
#Plot the lower flux boxplot
fig = plt.figure()
ax = plt.subplot(1,1,1)
plot_bins = [[] for i in (time_unique)]
for i in range(0,len(time_unique)):
    temp_bins=eroded_bins[(eroded_bins['time'] == time_unique[i]) & (eroded_bins['bn'] == eroded_bins.bn.max())]
    plot_bins[i] = np.append(plot_bins[i], [temp_bins['c_conc']])

ax.boxplot(plot_bins,showfliers=False,labels=timelabels)
ax.set_ylabel('$^1$$^4$C Concentration (atoms g$^-$$^1$)',fontsize=20)
ax.set_xlabel('Age (kiloyears)',fontsize=20)
plt.tight_layout()
plt.savefig(DataDirectory+'hillslope_carbon14_conc_flux_output', dpi=100, bbox_inches='tight')



fig = plt.figure()
ax = plt.subplot(1,1,1)

plot_bins = [[] for i in (time_unique)]
for i in range(0,len(time_unique)):
    temp_bins=eroded_bins[(eroded_bins['time'] == time_unique[i]) & (eroded_bins['bn'] == eroded_bins.bn.max())]
    plot_bins[i] = np.append(plot_bins[i], [temp_bins['c_conc']])

ax.violinplot(plot_bins,showextrema=False,showmedians=True,positions=timelabels,widths=0.5*timelabels[0])
ax.set_ylabel('$^1$$^4$C Concentration (atoms g$^-$$^1$)',fontsize=20)
ax.set_xlabel('Age (kiloyears)',fontsize=20)
plt.tight_layout()
plt.savefig(DataDirectory+'hillslope_carbon14_conc_flux_output_violin', dpi=100, bbox_inches='tight')


