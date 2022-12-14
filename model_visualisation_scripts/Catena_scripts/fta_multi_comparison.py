#IMport the pacakges
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from itertools import repeat
from matplotlib.cm import ScalarMappable
#Import the data_
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/steady_state_tests/analytical_linear_test/'
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/feather_runs/fta/fta_linear_ss_surf/'
print('This is the input file directory: '+DataDirectory)
#Load all the data
print('Load the flowtube data')
ft_out = pd.read_csv(DataDirectory+'ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )

print('Load the particle data')
bins = pd.read_csv(DataDirectory+'p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )


# original elev data
prof_in = pd.read_csv(DataDirectory+'profile.sm',header=None,delim_whitespace=True,names=['temp1','temp2','temp3','elev','thick'])


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
pits = int(len(ft_pits))



time_unique = bins.time.unique()
time_unique = np.array(time_unique)
time_unique = time_unique/1000
timelabels = time_unique
bins_unique = bins.bn.unique()
bins_unique = np.array(bins_unique)
bins['time'] = bins['time']/1000



colors = plt.cm.viridis(np.linspace(0,1,len(time_unique)))


cosmo_data = pd.read_csv('/exports/csce/datastore/geos/users/s0933963/feather_river_mixing_paper/Cosmo_spreadsheets/fta_cosmo.csv',sep=",",header=0,names=['Sample_Code','Pit','DS_dist','Start_d','End_d','Horizon','Be_conc','Be_error'] )
cosmo_pits = cosmo_data.Pit.unique()
cosmo_pits = np.array(cosmo_pits)
cosmo_pits = cosmo_pits.astype(np.float)


pit_data = pd.read_csv('/exports/csce/datastore/geos/users/s0933963/github/ModelTesting/flowtube_testing/fta_sites_csv.txt',sep=",",header=0,names=['X_coord','Y_coord','PIT_REF','elev','soil_thick'] )

pit_data['PIT_REF'] = pit_data['PIT_REF'].astype(str).str.replace('FTA-','').astype(float)


depth = np.arange(0,2,0.1)
density = np.full_like(depth,1325)
dloc = depth*density*0.1
gamma = [160,1459.76761923,11039.2402217,4320]
scaling = [1.6257852,0.014495419,0.0025436458,0]
lambda_s = 500*np.power(10.0,-9)
erosion = 0.0022
p_0 = 4.075213
cum_tot=0
for i in range (0,4):
    tot = (np.exp(-dloc/gamma[i])*scaling[i]*gamma[i])/(erosion+gamma[i]*lambda_s)
    cum_tot = cum_tot+(tot*p_0)

cum_tot_new = 0
erosion = 0.011396
for i in range (0,4):
    tot = (np.exp(-dloc/gamma[i])*scaling[i]*gamma[i])/(erosion+gamma[i]*lambda_s)
    cum_tot_new = cum_tot_new+(tot*p_0)







bin_index= []
# Get the bin data for each
for j in range(0,len(cosmo_pits)):
    # Find the point in the particle list that closely matches the elevation
    index_height = pit_data[(pit_data.PIT_REF == cosmo_pits[j])]
    height = index_height.elev.values[0]
    bindex = prof_in['elev'].sub(height).abs().idxmin()
    bin_index.append(bindex)




fig = plt.figure(figsize =(20,16))



for i in range(0,len(time_unique)):
    t = time_unique[i]*1000
    thick = ft_data[i*pits:i*pits+pits][:,5]
    for j in range(0,len(bin_index)):
        ax = plt.subplot(2,len(bin_index),j+1)

        ax.ticklabel_format(axis='x',style='sci',scilimits=(0,0))
        temp_cosmo = cosmo_data[(cosmo_data['Pit'] == cosmo_pits[j])]
        err = (temp_cosmo.End_d-temp_cosmo.Start_d)/2/100
        ax.errorbar(temp_cosmo.Be_conc,(temp_cosmo.Start_d+temp_cosmo.End_d)/2/100,yerr=err,xerr=temp_cosmo.Be_error,fmt='none',c='k',ls='--')
        ax.scatter(temp_cosmo.Be_conc,(temp_cosmo.Start_d+temp_cosmo.End_d)/2/100,s=10.0)
        for k in range(0,len(temp_cosmo['Start_d'])):
            # print(temp_cosmo['End_d'].values[k]/100)
            temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['bn'] >= bin_index[j]*2) & (bins['bn'] <= bin_index[j]*2+1) & (bins['d_loc'] >= temp_cosmo['Start_d'].values[k]/100) & (bins['d_loc'] <= temp_cosmo['End_d'].values[k]/100)]
            cb = ax.scatter(temp_bins.be_conc.mean(),((temp_cosmo['End_d'].values[k]+temp_cosmo['Start_d'].values[k])/2/100),color=colors[i],s=10.0)
            ax.set_ylim(0,temp_cosmo['End_d'].values[k]/100)
        ax.set_xlim(0,600000)
        ax.ticklabel_format(axis='x',style='sci',scilimits=(0,0))
        plt.gca().invert_yaxis()
        ax.set_title('Pit '+str(j+1)+' ('+str(((bin_index[j]*2+bin_index[j]*2))/4)+'m downslope)',fontsize=12)
        ax.plot(cum_tot,depth,c='grey',alpha = 0.5,ls='--',label='POMD erosion rate')
        ax.plot(cum_tot_new,depth,c='grey',alpha=0.5,ls='-.',label='BRC erosion rate')
        # if i == 0:
        #     ax.legend(loc=4)


DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/feather_runs/fta/fta_nonlinear_ss_surf/'
print('This is the input file directory: '+DataDirectory)
#Load all the data
print('Load the flowtube data')
ft_out = pd.read_csv(DataDirectory+'ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )

print('Load the particle data')
bins = pd.read_csv(DataDirectory+'p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )


# original elev data
prof_in = pd.read_csv(DataDirectory+'profile.sm',header=None,delim_whitespace=True,names=['temp1','temp2','temp3','elev','thick'])


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
pits = int(len(ft_pits))



time_unique = bins.time.unique()
time_unique = np.array(time_unique)
time_unique = time_unique/1000
timelabels = time_unique
bins_unique = bins.bn.unique()
bins_unique = np.array(bins_unique)
bins['time'] = bins['time']/1000



colors = plt.cm.viridis(np.linspace(0,1,len(time_unique)))


cosmo_data = pd.read_csv('/exports/csce/datastore/geos/users/s0933963/feather_river_mixing_paper/Cosmo_spreadsheets/fta_cosmo.csv',sep=",",header=0,names=['Sample_Code','Pit','DS_dist','Start_d','End_d','Horizon','Be_conc','Be_error'] )
cosmo_pits = cosmo_data.Pit.unique()
cosmo_pits = np.array(cosmo_pits)
cosmo_pits = cosmo_pits.astype(np.float)


pit_data = pd.read_csv('/exports/csce/datastore/geos/users/s0933963/github/ModelTesting/flowtube_testing/fta_sites_csv.txt',sep=",",header=0,names=['X_coord','Y_coord','PIT_REF','elev','soil_thick'] )

pit_data['PIT_REF'] = pit_data['PIT_REF'].astype(str).str.replace('FTA-','').astype(float)


depth = np.arange(0,2,0.1)
density = np.full_like(depth,1325)
dloc = depth*density*0.1
gamma = [160,1459.76761923,11039.2402217,4320]
scaling = [1.6257852,0.014495419,0.0025436458,0]
lambda_s = 500*np.power(10.0,-9)
erosion = 0.0022
p_0 = 4.075213
cum_tot=0
for i in range (0,4):
    tot = (np.exp(-dloc/gamma[i])*scaling[i]*gamma[i])/(erosion+gamma[i]*lambda_s)
    cum_tot = cum_tot+(tot*p_0)

cum_tot_new = 0
erosion = 0.011396
for i in range (0,4):
    tot = (np.exp(-dloc/gamma[i])*scaling[i]*gamma[i])/(erosion+gamma[i]*lambda_s)
    cum_tot_new = cum_tot_new+(tot*p_0)







bin_index= []
# Get the bin data for each
for j in range(0,len(cosmo_pits)):
    # Find the point in the particle list that closely matches the elevation
    index_height = pit_data[(pit_data.PIT_REF == cosmo_pits[j])]
    height = index_height.elev.values[0]
    bindex = prof_in['elev'].sub(height).abs().idxmin()
    bin_index.append(bindex)








for i in range(0,len(time_unique)):
    t = time_unique[i]*1000
    thick = ft_data[i*pits:i*pits+pits][:,5]
    for j in range(0,len(bin_index)):
        ax = plt.subplot(2,len(bin_index),j+len(bin_index)+1)

        ax.ticklabel_format(axis='x',style='sci',scilimits=(0,0))
        temp_cosmo = cosmo_data[(cosmo_data['Pit'] == cosmo_pits[j])]
        err = (temp_cosmo.End_d-temp_cosmo.Start_d)/2/100
        ax.errorbar(temp_cosmo.Be_conc,(temp_cosmo.Start_d+temp_cosmo.End_d)/2/100,yerr=err,xerr=temp_cosmo.Be_error,fmt='none',c='k',ls='--')
        ax.scatter(temp_cosmo.Be_conc,(temp_cosmo.Start_d+temp_cosmo.End_d)/2/100,s=10.0)
        for k in range(0,len(temp_cosmo['Start_d'])):
            # print(temp_cosmo['End_d'].values[k]/100)
            temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['bn'] >= bin_index[j]*2) & (bins['bn'] <= bin_index[j]*2+1) & (bins['d_loc'] >= temp_cosmo['Start_d'].values[k]/100) & (bins['d_loc'] <= temp_cosmo['End_d'].values[k]/100)]
            cb = ax.scatter(temp_bins.be_conc.mean(),((temp_cosmo['End_d'].values[k]+temp_cosmo['Start_d'].values[k])/2/100),color=colors[i],s=10.0)
            ax.set_ylim(0,temp_cosmo['End_d'].values[k]/100)
        ax.set_xlim(0,600000)
        ax.ticklabel_format(axis='x',style='sci',scilimits=(0,0))
        plt.gca().invert_yaxis()
        # ax.set_title('Pit '+str(j+1)+' ('+str(((bin_index[j]*2+bin_index[j]*2))/4)+'m downslope)',fontsize=12)
        ax.plot(cum_tot,depth,c='grey',alpha = 0.5,ls='--',label='POMD erosion rate')
        ax.plot(cum_tot_new,depth,c='grey',alpha=0.5,ls='-.',label='BRC erosion rate')
        if i == 0 and j == len(bin_index)-1:
            ax.legend(loc=1, prop={'size': 12})



cb.set_clim(vmin=0,vmax=max(time_unique))
fig.subplots_adjust(right=0.85)
cbar_ax = fig.add_axes([0.9, 0.1, 0.02, 0.78])
axcb = plt.colorbar(ScalarMappable(cmap=cb.get_cmap(), norm=cb.norm), cax=cbar_ax)
axcb.ax.set_ylabel('Time (kiloyears)',fontsize=12)

ax =fig.add_subplot(1,1,1,frameon=False)
ax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
ax.set_ylabel('Depth (m)',fontsize=18)
    
ax.set_xlabel('$^1$$^0$Be Concentration atoms g$^-$$^1$',fontsize=18)

ax.xaxis.labelpad = 20
# plt.show()
# plt.tight_layout()
plt.savefig(DataDirectory+'fta_crn_pits_combined.png', dpi=100, bbox_inches='tight')
  
        








