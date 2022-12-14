
#IMport the pacakges
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from itertools import repeat
#Import the data_
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/steady_state_tests/analytical_linear_test/'
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/sensitivity_tests/particle_inserts/particle_insert_2/'
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
# print(bins)
# for i in range(0,len(time_unique)):
#     thick = ft_data[i*pits:i*pits+pits][:,5]
#     thick = [x for item in thick for x in repeat(item,2)]
#     for j in range(0,len(bins_unique)):
#         bins = bins.drop(bins[(bins['time'] == time_unique[i]) & (bins['bn'] == bins_unique[j]) & (bins['d_loc'] <= thick[j])].index)
# print(bins)




# for j in range(0,len(time_unique)):
for j in range(0,1):
    ft_data_temp = ft_data[j*pits:j*pits+pits][:,:]
    fig = plt.figure()
    ax =plt.axes(projection='3d',computed_zorder=False)
    for i in range(1,2):
        thick = ft_data[i*pits:i*pits+pits][:,5]
        thick = [x for item in thick for x in repeat(item,2)]
        temp_bins1 = bins[(bins['time'] == time_unique[j]) & (bins['bn'] >= (i)-1) & (bins['bn'] <= (i)) & (bins['d_loc'] <= thick[i]+3.0)]
        # temp_bins1 = temp_bins.sample(n=20000,random_state=1)
        max = temp_bins1.be_conc.max()
        min = temp_bins1.be_conc.min()
        print(max)
        print(min)
    
        # thick = ft_data[i*pits:i*pits+pits][:,5]
        # thick = [x for item in thick for x in repeat(item,2)]
        # for j in range(0,len(bins_unique)):
            
        #     temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['bn'] == bins_unique[j]) & (bins['d_loc'] <= thick[j])]
        for idx, row in temp_bins1.iterrows():
            s_loc = row.s_loc
            z_loc = row.z_loc            
            be_conc = row.be_conc
            # ax.scatter(s_loc,np.random.random()*1,z_loc,c=row.be_conc,s=0.5,cmap='YlOrBr',vmin=min,vmax=max,zorder=1) 
            cb = ax.scatter(s_loc,np.random.random()*1,z_loc,c=row.be_conc,s=0.25,cmap='viridis',vmin=min,vmax=max,zorder=1)   

for j in range(0,1):
    ft_data_temp = ft_data[j*pits:j*pits+pits][:,:]
    
    for i in range(1,2):           
            # Draw the outline
        line1x = [ft_data_temp[i-1,0]-0.5,ft_data_temp[i,0]-0.5]
        line1y = [0,0]        
        line1z = [ft_data_temp[i-1,3],ft_data_temp[i,3]]
            
        line2x = [ft_data_temp[i-1,0]-0.5,ft_data_temp[i,0]-0.5]
        line2y = [0,0]        
        line2z = [ft_data_temp[i-1,4],ft_data_temp[i,4]]
        
        line3x = [ft_data_temp[i-1,0]-0.5,ft_data_temp[i,0]-0.5]
        line3y = [0+ft_data_temp[i-1,1],0+ft_data_temp[i,1]]
        line3z = [ft_data_temp[i-1,3],ft_data_temp[i,3]]

        line4x = [ft_data_temp[i-1,0]-0.5,ft_data_temp[i,0]-0.5]
        line4y = [0+ft_data_temp[i-1,1],0+ft_data_temp[i,1]]
        line4z = [ft_data_temp[i-1,4],ft_data_temp[i,4]]
            

        ax.plot(line1x,line1y,line1z,c='k',zorder=3)
        ax.plot(line2x,line2y,line2z,c='k',zorder=3)
        ax.plot(line3x,line3y,line3z,c='k',zorder=3)
        ax.plot(line4x,line4y,line4z,c='k',zorder=3)

        if i == 1:
            ax.plot([ft_data_temp[i-1,0]-0.5,ft_data_temp[i-1,0]-0.5],[0,0],[ft_data_temp[i-1,3],ft_data_temp[i-1,4]],c='k',zorder=3)
            ax.plot([ft_data_temp[i-1,0]-0.5,ft_data_temp[i-1,0]-0.5],[0+ft_data_temp[i-1,1],0+ft_data_temp[i,1]],[ft_data_temp[i-1,3],ft_data_temp[i-1,4]],c='k',zorder=3)
            ax.plot([ft_data_temp[i-1,0]-0.5,ft_data_temp[i-1,0]-0.5],[0,0+ft_data_temp[i-1,1]],[ft_data_temp[i-1,3],ft_data_temp[i-1,3]],c='k',zorder=3)
            ax.plot([ft_data_temp[i-1,0]-0.5,ft_data_temp[i-1,0]-0.5],[0,0+ft_data_temp[i,1]],[ft_data_temp[i-1,4],ft_data_temp[i-1,4]],c='k',zorder=3)
            ax.plot([ft_data_temp[i,0]-0.5,ft_data_temp[i,0]-0.5],[0,0],[ft_data_temp[i,3],ft_data_temp[i,4]],c='k',zorder=3)
            ax.plot([ft_data_temp[i,0]-0.5,ft_data_temp[i,0]-0.5],[0+ft_data_temp[i-1,1],0+ft_data_temp[i,1]],[ft_data_temp[i,3],ft_data_temp[i,4]],c='k',zorder=3)
            ax.plot([ft_data_temp[i,0]-0.5,ft_data_temp[i,0]-0.5],[0,0+ft_data_temp[i,1]],[ft_data_temp[i,3],ft_data_temp[i,3]],c='k',zorder=3)
            ax.plot([ft_data_temp[i,0]-0.5,ft_data_temp[i,0]-0.5],[0,0+ft_data_temp[i,1]],[ft_data_temp[i,4],ft_data_temp[i,4]],c='k',zorder=3)
        
    axcb = plt.colorbar(cb,orientation='horizontal',fraction=0.046,pad=0.2)
    axcb.ax.set_xlabel('$^1$$^0$Be Concentration atoms g$^-$$^1$',fontsize=10)
    ax.set_zlabel('Elevation (m)',fontsize=10)
    ax.set_ylabel('Distance along width (m)',fontsize=10)
    ax.set_xlabel('Distance Downslope (m)',fontsize=10)
    ax.xaxis.set_pane_color((1.0,1.0,1.0,0.0))
    ax.yaxis.set_pane_color((1.0,1.0,1.0,0.0))
    ax.zaxis.set_pane_color((1.0,1.0,1.0,0.0))

    ax.xaxis._axinfo["grid"]['color'] = (1,1,1,0)
    ax.yaxis._axinfo["grid"]['color'] = (1,1,1,0)
    ax.zaxis._axinfo["grid"]['color'] = (1,1,1,0)
    # z_max = np.max(ft_data_temp[:,4])
    # z_min = np.max(ft_data_temp[:,4]-2)
    # ax.set_zlim(z_max,z_min)
    # ax.invert_zaxis()


    plt.savefig(DataDirectory+'column_render_'+str(time_unique[j])+'.png', dpi=100, bbox_inches='tight')
# plt.show()
# plt.savefig(DataDirectory+'/test_render.png', dpi=100, bbox_inches='tight')