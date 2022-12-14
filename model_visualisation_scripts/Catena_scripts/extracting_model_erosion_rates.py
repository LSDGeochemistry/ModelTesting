import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from itertools import repeat


#Import the data_
folname = '10mm_mixing_full_cosmo'
dirname = '0_1mm_nonlinear'
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/changing_base_level/'+dirname+'/'+folname+'/'

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


# Read in data
# base level file
bl_in = pd.read_csv(DataDirectory+'base_level_hist.param',header=None ,sep=" ")

bl_counter = 0
bl_age = bl_in[bl_counter][0]
bl_old_c = 0
bl_counter = 0

# original elev data
prof_in = pd.read_csv(DataDirectory+'profile.sm',header=None,delim_whitespace=True)
# erosion rate file
er_in = pd.read_csv(DataDirectory+'erate_hist.param',header=None, sep=" ")
erosion_counter = 0
erosion_age = er_in[erosion_counter][0]
erosion = er_in[erosion_counter+1][0]

# sed trans file
sed_trans_in = pd.read_csv(DataDirectory+'sed_trans_param.stparam',header=None, sep=" ")
K = sed_trans_in[1][2]
p_0 = sed_trans_in[1][4]
gamma =  sed_trans_in[1][5]
# model run
model_run_in = pd.read_csv(DataDirectory+'model_run.param',header=None, sep=" ")
final_node = model_run_in[1][17]

model_erosion_fname = DataDirectory+'model_erosion_data_'+str(dirname)+'_'+str(folname)
file = open('%s' % model_erosion_fname, 'w')

# Set up the plots based on times
for i in range(0,len(time_unique)):
    fig = plt.figure()
    ax = plt.subplot(1,1,1)
    print(i)
    if time_unique[i]*1000 > erosion_age:
        erosion_counter = erosion_counter+2
    if time_unique[i]*1000 > bl_age:
        diff = time_unique[i]*1000-bl_age
        bl_old_c = bl_counter
        bl_counter = bl_counter+2 
    else:
        diff = 0  
    final_node = final_node-((time_unique[i]-(time_unique[0]*i))*1000-diff)*bl_in[bl_old_c+1][0]-(diff*bl_in[bl_counter+1][0])
    final_node = np.around(final_node,3)
    

    
    bl_old_c = bl_counter
    bl_age = bl_in[bl_counter][0]
    
    

    ds_dist = ft_data[i*pits:i*pits+pits][:,0]
    elev_old = prof_in[3][:]-min(prof_in[3][:])+1000
    
    elev = ft_data[i*pits:i*pits+pits][:,3]
    if i == 0:
        lowering = (elev_old-elev)/(time_unique[0]*1000)
        
    else:
        lowering = (ft_data[(i-1)*pits:(i-1)*pits+pits][:,3]-elev)/((time_unique[i]-time_unique[i-1])*1000)

    thick = ft_data[i*pits:i*pits+pits][:,5]
    
    width = ft_data[i*pits:i*pits+pits][:,1]
    slope = np.zeros(len(elev))
    flux = np.zeros(len(elev))
    t = np.zeros(len(elev))
    low = np.zeros(len(elev))
    for j in range(0,len(elev)-1):
        slope[j] = (elev[j]-elev[j+1])/(ds_dist[j+1]-ds_dist[j])

    slope[len(slope)-1] = (elev[len(slope)-1]-final_node)/(ds_dist[len(slope)-1]-ds_dist[len(slope)-2])
    slope = np.around(slope,3)
    flux[0]= K*thick[0]*width[0]*slope[0]

    for j in range(1,len(flux)):
        flux[j] = (K*thick[j]*width[j]*slope[j])-(K*thick[j-1]*width[j-1]*slope[j-1])
    
    for j in range(0,len(flux)):
        # t[j] = thick[j]/(flux[j]+erosion)
        flux[j] = flux[j]/(sed_trans_in[1][1]/sed_trans_in[1][0])
        low[j] = p_0*np.exp(-thick[j]/gamma)
    
        file.write(str(ds_dist[j]) + ' '+ str(elev[j])+  ' '  + str(width[j]) + ' ' + str(thick[j]) + ' ' + str(slope[j]) + ' '+ str(K) + ' '+ str(flux[j]) +' ' + str(low[j]) +'\n')

    # t = thick/((lowering+erosion)*(sed_trans_in[1][1]/sed_trans_in[1][0]))
    

    # cb = ax.scatter(ds_dist,t,s=3)
    # for j in range(0,len(ds_dist)):
    #     temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['bn'] >= bins_unique[j*2]) & (bins['bn'] <= bins_unique[j*2+1]) & (bins['d_loc'] <= thick[i])]
    #     mean_crn = temp_bins.mean().page
    #     cb = ax.scatter(ds_dist[j],mean_crn,s=3,marker='X',c='k')
   
    # ax.set_ylabel('Turnover time (yrs)',fontsize=16)
    # ax.set_xlabel('Distance Downslope (m)',fontsize=16)
    

    # plt.tight_layout()
    # plt.savefig(DataDirectory+'/hillslope_turnover_vs_mean_age_new'+str(int(time_unique[i]))+'.png', dpi=100, bbox_inches='tight')
file.close()