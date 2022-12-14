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






# sed trans file
sed_trans_in = pd.read_csv(DataDirectory+'sed_trans_param.stparam',header=None, sep=" ")
rho = sed_trans_in[1][0]/1000
# model run
model_run_in = pd.read_csv(DataDirectory+'model_run.param',header=None, sep=" ")
final_node = model_run_in[1][17]
# CRN param
crn_param_in = pd.read_csv(DataDirectory+'CRN_trans_param.CRNparam',header=None, sep=" ")
lat = crn_param_in[1][21]
lon = crn_param_in[1][22]
elev = crn_param_in[1][23]

# User defined variables 
thickness=0.1
mthd = 'std'
mineral = 'quartz'
shielding= '1'
erosion=0.001
sample = 'test'






# Write the first line

cronus_fname = DataDirectory+'for_cronus_data_'+str(dirname)+'_'+str(folname)
file = open('%s' % cronus_fname, 'w')
file.write(str(sample) + ' ' + str(lat) + ' ' + str(lon) + ' ' + str(elev) + ' ' + str(mthd) + ' ' + str(thickness) + ' ' + str(rho) + ' ' + str(shielding) + ' ' + str(erosion) + ' '+ '2010' +';'+'\n')

# Set up the rest of the dataframe



# Find the local (current) erosion rate



# Loop through the data
for i in range(0,len(time_unique)):

    thick = ft_data[i*pits:i*pits+pits][:,5]
    
    for j in range(0,len(bins_unique)//2):
        
        temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['bn'] >= bins_unique[j*2]) & (bins['bn'] <= bins_unique[j*2+1]) & (bins['d_loc'] > 0.0) & (bins['d_loc'] < 0.006)]
        
        mean_crn = temp_bins.mean().be_conc
        std_dv = temp_bins.std().be_conc
        file.write(str(sample) + ' ' + 'Be-10 ' + ' ' + str(mineral) + ' ' + str(mean_crn) + ' ' + str(std_dv) + ' '+ 'KNSTD' +';'+'\n')




file.close()











