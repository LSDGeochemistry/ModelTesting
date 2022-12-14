#Script for plotting and comparing down  ahillsope transect
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob

###User defined parameter for plotting
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/no_mixing/'
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/hillslope_flux_test/no_mixing_erosion_0_00001/'
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/mixing_0_0001/'
# DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/mixing_0_0001_erosion_0_001/'
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/changing_base_level/0_1mm_erosion/1mm_mixing'
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/steady_state_tests/analytical_nonlinear_test/'
#

print('This is the input file directory: '+DataDirectory)
bins = pd.read_csv(DataDirectory+'/p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
print('loaded the particle file')
max_conc = (bins['be_conc']).max()

# Set unique times
time_unique = bins.time.unique()
time_unique = np.array(time_unique)
# Set up the ds distances
ft_out = pd.read_csv(DataDirectory+'/ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )
ft_pits = ft_out.s.unique()
ft_pits = np.array(ft_pits)
ft_pits = np.delete(ft_pits, np.where(ft_pits == '-99'))
ft_pits = np.delete(ft_pits, np.where(ft_pits == 's'))
ft_pits = ft_pits.astype(np.float)
ft_pits =[min(ft_pits),max(ft_pits)*0.25,max(ft_pits)*0.5,max(ft_pits)*0.75,max(ft_pits)]
# Set up the bin intervals
depth_bins =[[0,0.1],[0.1,0.2],[0.2,0.3],[0.3,0.4],[0.4,0.5],[0.5,0.6],[0.6,0.7],[0.7,0.8],[0.8,0.9],[0.9,1.0]]

# Set up the plots based on times
for i in range(0,len(time_unique)):
    fig = plt.figure(figsize =(15,6))

    # Set up the different pits and plot
    for j in range(0,len(ft_pits)):
        upp = ft_pits[j]+0.5
        low = ft_pits[j]-0.5
        temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['s_loc'] <= upp) & (bins['s_loc'] >= low)]
        # Set up the plot
        ax = plt.subplot(1,len(ft_pits),j+1)
        ax.scatter(temp_bins.be_conc,temp_bins.d_loc,c='0.6',s=0.05)
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
            
            ax.set_ylim(0,1.0)
            ax.set_xlim(0,50000)
            plt.gca().invert_yaxis()
            ax.set_title('Pit '+str(j+1)+' ('+str(ft_pits[j])+'m downslope)',fontsize=12)
            if j > 0:
                ax.set_yticklabels([])


    ax =fig.add_subplot(1,1,1,frameon=False)
    ax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    ax.set_ylabel('Depth (m)',fontsize=18)
    
    ax.set_xlabel('$^1$$^0$Be Concentration atoms g$^-$$^1$',fontsize=18)


    plt.tight_layout()
    plt.savefig(DataDirectory+'/hillslope_crn_conc_bins_depth_profile_binned_'+str(time_unique[i])+'.png', dpi=100, bbox_inches='tight')

#Output the Be concentration with depth for each bin and plot but onthe same plot coloured by bin


# Plot the analytical solution?
#Time (a)
# t = 10000
# #Production rate at surface (atoms/g/a) (taken from Table 6)
# p_0 = 2.41 #from LSD mixing model
# #Depth of profile (cm)
# d = 100
# #Depth profile for testing
# z = np.arange(0,d,0.1)
# #density of material (g/cm^3)
# rho = 2.0
# #density of quartz (g/cm^3)
# rho_q =2.65
# e = 0
# #Decay Constant
# gamma = 0
# #attenuation lenth (g/cm^2)
# l = 160 #from the LSD mixing model
# #Production rate at different depth each year
# p_z = p_0*np.exp(-rho*z/l)
# #Production for x number of years
# p_z_t = p_z*t
# ax.plot(p_z_t,z/100,label = 'Lal and Chen Analytical Model',c='k',linestyle='dashed')
# ax.set_xlim(0,max_conc)
# ax.set_ylim(0,1.0)
# plt.gca().invert_yaxis()
# ax.legend(loc='upper left',fontsize = 12)
# ax.title.set_text('Flat')
# # Do the shallow slope
#
# plt.savefig(DataDirectory+'hillslope_crn_conc_bins_depth_profile_binned', dpi=100, bbox_inches='tight')
#
#

