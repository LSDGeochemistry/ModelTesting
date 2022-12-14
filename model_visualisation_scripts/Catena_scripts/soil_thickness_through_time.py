#Script for plotting and comparing down  ahillsope transect
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from scipy.interpolate import make_interp_spline, BSpline

###User defined parameter for plotting
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/no_mixing/'
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/hillslope_flux_test/no_mixing_erosion_0_00001/'
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/mixing_0_0001/'
# DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/mixing_0_0001_erosion_0_001/'
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/steady_state_tests/analytical_nonlinear_test/'
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/changing_base_level/0_2mm_nonlinear/10mm_mixing'
#Number of profiles (bins), should rip this straight from model output for simplicity!!!

print('This is the input file directory: '+DataDirectory)

# Set up the ds distances
ft_out = pd.read_csv(DataDirectory+'/ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )
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
# print(ft_data)
fig = plt.figure()
ax = plt.subplot(1,1,1)
# Set up the plots based on times
for i in range(0,timesteps):


    # Set up the different pits and plot
    ds_dist = ft_data[i*pits:i*pits+pits][:,0]

    thick = ft_data[i*pits:i*pits+pits][:,5]
    
        # Now do the depth n_bins

    ax.scatter(ds_dist,thick,s=2,c='k')
        # ax.set_ylim(0,1.0)
        # ax.set_xlim(0,110000)
    # ds_dist = np.array(ds_dist)
    # elev = np.array(elev)
    # # print(ds_dist)
    # # print(elev)
    # hillslope_line = np.linspace(min(ds_dist),max(ds_dist),100)
    # if len(elev)>3:
    #     z_spl=make_interp_spline(ds_dist,elev,k=1)
    #
    # else:
    #     z_spl=make_interp_spline(ds_dist,elev,k=2)
    # zeta_smooth = z_spl(hillslope_line)
    # plt.plot(hillslope_line,zeta_smooth,linewidth=1,c='k',linestyle='dashed')

ax.set_ylabel('Soil Thickness (m)',fontsize=16)
ax.set_xlabel('Distance Downslope (m)',fontsize=16)
# ax.set_ylim(0,1.0)
    # ax.set_xlim(0,110000)

plt.tight_layout()

plt.savefig(DataDirectory+'/soil_thickness_with_time.png', dpi=100, bbox_inches='tight')
