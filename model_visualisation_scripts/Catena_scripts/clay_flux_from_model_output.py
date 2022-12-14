#IMport the pacakges
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import meshio
import warnings
warnings.filterwarnings("ignore")


# Import the data
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/test_vtk/steady_state_base_level/'
EpDataDirectory ='/exports/csce/datastore/geos/users/s0933963/test_vtk/steady_state_base_level_eroded_only/'
#Load all the data
ft_out = pd.read_csv(DataDirectory+'ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )

bins = pd.read_csv(EpDataDirectory+'ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )


# original sed trans
sed_trans_in = pd.read_csv(DataDirectory+'sed_trans_param.stparam',header=None, sep=" ")
# original model run (for base level)
model_run_in = pd.read_csv(DataDirectory+'model_run.param',header=None, sep=" ")
# crn file
crn_in = pd.read_csv(DataDirectory+'CRN_trans_param.CRNparam',header=None, sep=" ")

# erosion rate file
er_in = pd.read_csv(DataDirectory+'erate_hist.param',header=None, sep=" ")
erosion_counter = 0
erosion_age = er_in[erosion_counter][0]
erosion = er_in[erosion_counter+1][0]
# base level file
bl_in = pd.read_csv(DataDirectory+'base_level_hist.param',header=None ,sep=" ")

bl_counter = 0
bl_age = bl_in[bl_counter][0]
bl_old_c = 0
bl_counter = 0


# Set up some parameters
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
time_unique = time_unique
timelabels = time_unique
bins_unique = bins.bn.unique()
bins_unique = np.array(bins_unique)
bins['time'] = bins['time']
div = max(bins_unique)/max(ft_pits)
# Calculate the sediment flux

flux = np.zeros(len(time_unique))
final_node = model_run_in[1][17]
for i in range(0,len(time_unique)):
    # find the new bl
    
    if time_unique[i] > erosion_age:
        erosion_counter = erosion_counter+2
    if time_unique[i] > bl_age:
        diff = time_unique[i]-bl_age
        bl_old_c = bl_counter
        bl_counter = bl_counter+2 
    else:
        diff = 0  

    final_node = final_node-((time_unique[i]-(time_unique[0]*i))-diff)*bl_in[bl_old_c+1][0]-(diff*bl_in[bl_counter+1][0])

    # final_node = np.around(final_node,3)

    bl_old_c = bl_counter
    bl_age = bl_in[bl_counter][0]
    # find the slope
    ds_dist = ft_data[i*pits:i*pits+pits][:,0]
    elev = ft_data[i*pits:i*pits+pits][:,3]
    thick = ft_data[i*pits:i*pits+pits][:,5]
    width = ft_data[i*pits:i*pits+pits][:,1]

    slope = (elev[len(elev)-1]-final_node)/(ds_dist[len(ds_dist)-1]-ds_dist[len(ds_dist)-2])
    denom = 1/(1-slope*slope/(sed_trans_in[1][3]*sed_trans_in[1][3]))
    flux[i] = -sed_trans_in[1][0]*sed_trans_in[1][2]*thick[len(ds_dist)-1]*width[len(ds_dist)-1]*slope*denom

# Find number of depth intervals and their type
n_depth_intervals = int(crn_in[1][20])
depth_intervals = np.zeros((len(time_unique),n_depth_intervals+2))
for i in range(0,len(time_unique)):
    thick = ft_data[i*pits:i*pits+pits][:,5]
    depth_intervals[i] = np.linspace(0,thick[len(ds_dist)-1],num=n_depth_intervals+2)



frac = np.zeros((len(time_unique),n_depth_intervals))
flux_frac = np.zeros((len(time_unique)))
clay_flux = np.zeros((len(time_unique)))
# Find proportion of particles in each depth interval
for i in range(0,len(time_unique)):
    for j in range(0,n_depth_intervals):
        
        temp_bins = bins[(bins['time'] == time_unique[i])]
        total = len(temp_bins.be_conc) 
        temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['d_loc'] >= depth_intervals[i][j]) & (bins['d_loc'] <= depth_intervals[i][j+1])]
        temp_total = len(temp_bins.be_conc) 
        frac[i][j] = int(temp_total)/int(total)
       
# Find mass fraction of kaolinte in each depth interval
start = int(crn_in[1][20])+int(crn_in[1][21])
end = int(crn_in[1][20])

for i in range(0,len(time_unique)):
  # Read in the data
    filename='CRUNCH_cells'+str(time_unique[i])+".vtk"
    data  = meshio.read(DataDirectory+filename)
    k_mf = data.cell_data['Mineral_mass_fraction_Kaolinite']
    kmf = k_mf[0][-(start):-(end)]
    for j in range(0,n_depth_intervals):
        flux_frac[i] = flux_frac[i]+((frac[i][j])*kmf[j][0])
    clay_flux[i] = -(flux_frac[i]*flux[i])
ss_clay_flux_no_mix = clay_flux

# Import the data
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/test_vtk/steady_state_partial_mixing/'
EpDataDirectory ='/exports/csce/datastore/geos/users/s0933963/test_vtk/steady_state_base_level_eroded_only/'
#Load all the data
ft_out = pd.read_csv(DataDirectory+'ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )

bins = pd.read_csv(EpDataDirectory+'ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )


# original sed trans
sed_trans_in = pd.read_csv(DataDirectory+'sed_trans_param.stparam',header=None, sep=" ")
# original model run (for base level)
model_run_in = pd.read_csv(DataDirectory+'model_run.param',header=None, sep=" ")
# crn file
crn_in = pd.read_csv(DataDirectory+'CRN_trans_param.CRNparam',header=None, sep=" ")

# erosion rate file
er_in = pd.read_csv(DataDirectory+'erate_hist.param',header=None, sep=" ")
erosion_counter = 0
erosion_age = er_in[erosion_counter][0]
erosion = er_in[erosion_counter+1][0]
# base level file
bl_in = pd.read_csv(DataDirectory+'base_level_hist.param',header=None ,sep=" ")

bl_counter = 0
bl_age = bl_in[bl_counter][0]
bl_old_c = 0
bl_counter = 0


# Set up some parameters
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
time_unique = time_unique
timelabels = time_unique
bins_unique = bins.bn.unique()
bins_unique = np.array(bins_unique)
bins['time'] = bins['time']
div = max(bins_unique)/max(ft_pits)
# Calculate the sediment flux

flux = np.zeros(len(time_unique))
final_node = model_run_in[1][17]
for i in range(0,len(time_unique)):
    # find the new bl
    
    if time_unique[i] > erosion_age:
        erosion_counter = erosion_counter+2
    if time_unique[i] > bl_age:
        diff = time_unique[i]-bl_age
        bl_old_c = bl_counter
        bl_counter = bl_counter+2 
    else:
        diff = 0  

    final_node = final_node-((time_unique[i]-(time_unique[0]*i))-diff)*bl_in[bl_old_c+1][0]-(diff*bl_in[bl_counter+1][0])

    # final_node = np.around(final_node,3)

    bl_old_c = bl_counter
    bl_age = bl_in[bl_counter][0]
    # find the slope
    ds_dist = ft_data[i*pits:i*pits+pits][:,0]
    elev = ft_data[i*pits:i*pits+pits][:,3]
    thick = ft_data[i*pits:i*pits+pits][:,5]
    width = ft_data[i*pits:i*pits+pits][:,1]

    slope = (elev[len(elev)-1]-final_node)/(ds_dist[len(ds_dist)-1]-ds_dist[len(ds_dist)-2])
    denom = 1/(1-slope*slope/(sed_trans_in[1][3]*sed_trans_in[1][3]))
    flux[i] = -sed_trans_in[1][0]*sed_trans_in[1][2]*thick[len(ds_dist)-1]*width[len(ds_dist)-1]*slope*denom
    
# Find number of depth intervals and their type
n_depth_intervals = int(crn_in[1][20])
depth_intervals = np.zeros((len(time_unique),n_depth_intervals+2))
for i in range(0,len(time_unique)):
    thick = ft_data[i*pits:i*pits+pits][:,5]
    depth_intervals[i] = np.linspace(0,thick[len(ds_dist)-1],num=n_depth_intervals+2)



frac = np.zeros((len(time_unique),n_depth_intervals))
flux_frac = np.zeros((len(time_unique)))
clay_flux = np.zeros((len(time_unique)))
# Find proportion of particles in each depth interval
for i in range(0,len(time_unique)):
    for j in range(0,n_depth_intervals):
        
        temp_bins = bins[(bins['time'] == time_unique[i])]
        total = len(temp_bins.be_conc) 
        temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['d_loc'] >= depth_intervals[i][j]) & (bins['d_loc'] <= depth_intervals[i][j+1])]
        temp_total = len(temp_bins.be_conc) 
        frac[i][j] = int(temp_total)/int(total)
       
# Find mass fraction of kaolinte in each depth interval
start = int(crn_in[1][20])+int(crn_in[1][21])
end = int(crn_in[1][20])

for i in range(0,len(time_unique)):
  # Read in the data
    filename='CRUNCH_cells'+str(time_unique[i])+".vtk"
    data  = meshio.read(DataDirectory+filename)
    k_mf = data.cell_data['Mineral_mass_fraction_Kaolinite']
    kmf = k_mf[0][-(start):-(end)]
    for j in range(0,n_depth_intervals):
        flux_frac[i] = flux_frac[i]+((frac[i][j])*kmf[j][0])
    clay_flux[i] = -(flux_frac[i]*flux[i])
ss_clay_flux_part_mix = clay_flux
# Import the data
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/test_vtk/steady_state_full_mixing/'
EpDataDirectory ='/exports/csce/datastore/geos/users/s0933963/test_vtk/steady_state_base_level_eroded_only/'
#Load all the data
ft_out = pd.read_csv(DataDirectory+'ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )

bins = pd.read_csv(EpDataDirectory+'ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )


# original sed trans
sed_trans_in = pd.read_csv(DataDirectory+'sed_trans_param.stparam',header=None, sep=" ")
# original model run (for base level)
model_run_in = pd.read_csv(DataDirectory+'model_run.param',header=None, sep=" ")
# crn file
crn_in = pd.read_csv(DataDirectory+'CRN_trans_param.CRNparam',header=None, sep=" ")

# erosion rate file
er_in = pd.read_csv(DataDirectory+'erate_hist.param',header=None, sep=" ")
erosion_counter = 0
erosion_age = er_in[erosion_counter][0]
erosion = er_in[erosion_counter+1][0]
# base level file
bl_in = pd.read_csv(DataDirectory+'base_level_hist.param',header=None ,sep=" ")

bl_counter = 0
bl_age = bl_in[bl_counter][0]
bl_old_c = 0
bl_counter = 0


# Set up some parameters
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
time_unique = time_unique
timelabels = time_unique
bins_unique = bins.bn.unique()
bins_unique = np.array(bins_unique)
bins['time'] = bins['time']
div = max(bins_unique)/max(ft_pits)
# Calculate the sediment flux

flux = np.zeros(len(time_unique))
final_node = model_run_in[1][17]
for i in range(0,len(time_unique)):
    # find the new bl
    
    if time_unique[i] > erosion_age:
        erosion_counter = erosion_counter+2
    if time_unique[i] > bl_age:
        diff = time_unique[i]-bl_age
        bl_old_c = bl_counter
        bl_counter = bl_counter+2 
    else:
        diff = 0  

    final_node = final_node-((time_unique[i]-(time_unique[0]*i))-diff)*bl_in[bl_old_c+1][0]-(diff*bl_in[bl_counter+1][0])

    # final_node = np.around(final_node,3)

    bl_old_c = bl_counter
    bl_age = bl_in[bl_counter][0]
    # find the slope
    ds_dist = ft_data[i*pits:i*pits+pits][:,0]
    elev = ft_data[i*pits:i*pits+pits][:,3]
    thick = ft_data[i*pits:i*pits+pits][:,5]
    width = ft_data[i*pits:i*pits+pits][:,1]

    slope = (elev[len(elev)-1]-final_node)/(ds_dist[len(ds_dist)-1]-ds_dist[len(ds_dist)-2])
    denom = 1/(1-slope*slope/(sed_trans_in[1][3]*sed_trans_in[1][3]))
    flux[i] = -sed_trans_in[1][0]*sed_trans_in[1][2]*thick[len(ds_dist)-1]*width[len(ds_dist)-1]*slope*denom
    
# Find number of depth intervals and their type
n_depth_intervals = int(crn_in[1][20])
depth_intervals = np.zeros((len(time_unique),n_depth_intervals+2))
for i in range(0,len(time_unique)):
    thick = ft_data[i*pits:i*pits+pits][:,5]
    depth_intervals[i] = np.linspace(0,thick[len(ds_dist)-1],num=n_depth_intervals+2)



frac = np.zeros((len(time_unique),n_depth_intervals))
flux_frac = np.zeros((len(time_unique)))
clay_flux = np.zeros((len(time_unique)))
# Find proportion of particles in each depth interval
for i in range(0,len(time_unique)):
    for j in range(0,n_depth_intervals):
        
        temp_bins = bins[(bins['time'] == time_unique[i])]
        total = len(temp_bins.be_conc) 
        temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['d_loc'] >= depth_intervals[i][j]) & (bins['d_loc'] <= depth_intervals[i][j+1])]
        temp_total = len(temp_bins.be_conc) 
        frac[i][j] = int(temp_total)/int(total)
       
# Find mass fraction of kaolinte in each depth interval
start = int(crn_in[1][20])+int(crn_in[1][21])
end = int(crn_in[1][20])

for i in range(0,len(time_unique)):
  # Read in the data
    filename='CRUNCH_cells'+str(time_unique[i])+".vtk"
    data  = meshio.read(DataDirectory+filename)
    k_mf = data.cell_data['Mineral_mass_fraction_Kaolinite']
    kmf = k_mf[0][-(start):-(end)]
    for j in range(0,n_depth_intervals):
        flux_frac[i] = flux_frac[i]+((frac[i][j])*kmf[j][0])
    clay_flux[i] = -(flux_frac[i]*flux[i])

ss_clay_flux_full_mix = clay_flux

# Import the data
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/test_vtk/decrease_base_level/changing_base_level_decrease/'
EpDataDirectory ='/exports/csce/datastore/geos/users/s0933963/test_vtk/decrease_base_level/changing_base_level_decrease_eroded_only/'
#Load all the data
ft_out = pd.read_csv(DataDirectory+'ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )

bins = pd.read_csv(EpDataDirectory+'ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )


# original sed trans
sed_trans_in = pd.read_csv(DataDirectory+'sed_trans_param.stparam',header=None, sep=" ")
# original model run (for base level)
model_run_in = pd.read_csv(DataDirectory+'model_run.param',header=None, sep=" ")
# crn file
crn_in = pd.read_csv(DataDirectory+'CRN_trans_param.CRNparam',header=None, sep=" ")

# erosion rate file
er_in = pd.read_csv(DataDirectory+'erate_hist.param',header=None, sep=" ")
erosion_counter = 0
erosion_age = er_in[erosion_counter][0]
erosion = er_in[erosion_counter+1][0]
# base level file
bl_in = pd.read_csv(DataDirectory+'base_level_hist.param',header=None ,sep=" ")

bl_counter = 0
bl_age = bl_in[bl_counter][0]
bl_old_c = 0
bl_counter = 0


# Set up some parameters
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
time_unique = time_unique
timelabels = time_unique
bins_unique = bins.bn.unique()
bins_unique = np.array(bins_unique)
bins['time'] = bins['time']
div = max(bins_unique)/max(ft_pits)
# Calculate the sediment flux

flux = np.zeros(len(time_unique))
final_node = model_run_in[1][17]
for i in range(0,len(time_unique)):
    # find the new bl
    
    if time_unique[i] > erosion_age:
        erosion_counter = erosion_counter+2
    if time_unique[i] > bl_age:
        diff = time_unique[i]-bl_age
        bl_old_c = bl_counter
        bl_counter = bl_counter+2 
    else:
        diff = 0  

    final_node = final_node-((time_unique[i]-(time_unique[0]*i))-diff)*bl_in[bl_old_c+1][0]-(diff*bl_in[bl_counter+1][0])

    # final_node = np.around(final_node,3)

    bl_old_c = bl_counter
    bl_age = bl_in[bl_counter][0]
    # find the slope
    ds_dist = ft_data[i*pits:i*pits+pits][:,0]
    elev = ft_data[i*pits:i*pits+pits][:,3]
    thick = ft_data[i*pits:i*pits+pits][:,5]
    width = ft_data[i*pits:i*pits+pits][:,1]

    slope = (elev[len(elev)-1]-final_node)/(ds_dist[len(ds_dist)-1]-ds_dist[len(ds_dist)-2])
    denom = 1/(1-slope*slope/(sed_trans_in[1][3]*sed_trans_in[1][3]))
    flux[i] = -sed_trans_in[1][0]*sed_trans_in[1][2]*thick[len(ds_dist)-1]*width[len(ds_dist)-1]*slope*denom
  
# Find number of depth intervals and their type
n_depth_intervals = int(crn_in[1][20])
depth_intervals = np.zeros((len(time_unique),n_depth_intervals+2))
for i in range(0,len(time_unique)):
    thick = ft_data[i*pits:i*pits+pits][:,5]
    depth_intervals[i] = np.linspace(0,thick[len(ds_dist)-1],num=n_depth_intervals+2)



frac = np.zeros((len(time_unique),n_depth_intervals))
flux_frac = np.zeros((len(time_unique)))
clay_flux = np.zeros((len(time_unique)))
# Find proportion of particles in each depth interval
for i in range(0,len(time_unique)):
    for j in range(0,n_depth_intervals):
        
        temp_bins = bins[(bins['time'] == time_unique[i])]
        total = len(temp_bins.be_conc) 
        temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['d_loc'] >= depth_intervals[i][j]) & (bins['d_loc'] <= depth_intervals[i][j+1])]
        temp_total = len(temp_bins.be_conc) 
        frac[i][j] = int(temp_total)/int(total)
# Find mass fraction of kaolinte in each depth interval
start = int(crn_in[1][20])+int(crn_in[1][21])
end = int(crn_in[1][20])

for i in range(0,len(time_unique)):
  # Read in the data
    filename='CRUNCH_cells'+str(time_unique[i])+".vtk"
    data  = meshio.read(DataDirectory+filename)
    k_mf = data.cell_data['Mineral_mass_fraction_Kaolinite']
    kmf = k_mf[0][-(start):-(end)]
    for j in range(0,n_depth_intervals):
        flux_frac[i] = flux_frac[i]+((frac[i][j])*kmf[j][0])
    clay_flux[i] = -(flux_frac[i]*flux[i])
dbl_clay_flux_no_mix = clay_flux

# Import the data
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/test_vtk/decrease_base_level/changing_base_level_partial_mixing_decrease/'
EpDataDirectory ='/exports/csce/datastore/geos/users/s0933963/test_vtk/decrease_base_level/changing_base_level_decrease_eroded_only/'
#Load all the data
ft_out = pd.read_csv(DataDirectory+'ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )

bins = pd.read_csv(EpDataDirectory+'ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )


# original sed trans
sed_trans_in = pd.read_csv(DataDirectory+'sed_trans_param.stparam',header=None, sep=" ")
# original model run (for base level)
model_run_in = pd.read_csv(DataDirectory+'model_run.param',header=None, sep=" ")
# crn file
crn_in = pd.read_csv(DataDirectory+'CRN_trans_param.CRNparam',header=None, sep=" ")

# erosion rate file
er_in = pd.read_csv(DataDirectory+'erate_hist.param',header=None, sep=" ")
erosion_counter = 0
erosion_age = er_in[erosion_counter][0]
erosion = er_in[erosion_counter+1][0]
# base level file
bl_in = pd.read_csv(DataDirectory+'base_level_hist.param',header=None ,sep=" ")

bl_counter = 0
bl_age = bl_in[bl_counter][0]
bl_old_c = 0
bl_counter = 0


# Set up some parameters
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
time_unique = time_unique
timelabels = time_unique
bins_unique = bins.bn.unique()
bins_unique = np.array(bins_unique)
bins['time'] = bins['time']
div = max(bins_unique)/max(ft_pits)
# Calculate the sediment flux

flux = np.zeros(len(time_unique))
final_node = model_run_in[1][17]
for i in range(0,len(time_unique)):
    # find the new bl
    
    if time_unique[i] > erosion_age:
        erosion_counter = erosion_counter+2
    if time_unique[i] > bl_age:
        diff = time_unique[i]-bl_age
        bl_old_c = bl_counter
        bl_counter = bl_counter+2 
    else:
        diff = 0  

    final_node = final_node-((time_unique[i]-(time_unique[0]*i))-diff)*bl_in[bl_old_c+1][0]-(diff*bl_in[bl_counter+1][0])

    # final_node = np.around(final_node,3)

    bl_old_c = bl_counter
    bl_age = bl_in[bl_counter][0]
    # find the slope
    ds_dist = ft_data[i*pits:i*pits+pits][:,0]
    elev = ft_data[i*pits:i*pits+pits][:,3]
    thick = ft_data[i*pits:i*pits+pits][:,5]
    width = ft_data[i*pits:i*pits+pits][:,1]

    slope = (elev[len(elev)-1]-final_node)/(ds_dist[len(ds_dist)-1]-ds_dist[len(ds_dist)-2])
    denom = 1/(1-slope*slope/(sed_trans_in[1][3]*sed_trans_in[1][3]))
    flux[i] = -sed_trans_in[1][0]*sed_trans_in[1][2]*thick[len(ds_dist)-1]*width[len(ds_dist)-1]*slope*denom
    
# Find number of depth intervals and their type
n_depth_intervals = int(crn_in[1][20])
depth_intervals = np.zeros((len(time_unique),n_depth_intervals+2))
for i in range(0,len(time_unique)):
    thick = ft_data[i*pits:i*pits+pits][:,5]
    depth_intervals[i] = np.linspace(0,thick[len(ds_dist)-1],num=n_depth_intervals+2)



frac = np.zeros((len(time_unique),n_depth_intervals))
flux_frac = np.zeros((len(time_unique)))
clay_flux = np.zeros((len(time_unique)))
# Find proportion of particles in each depth interval
for i in range(0,len(time_unique)):
    for j in range(0,n_depth_intervals):
        
        temp_bins = bins[(bins['time'] == time_unique[i])]
        total = len(temp_bins.be_conc) 
        temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['d_loc'] >= depth_intervals[i][j]) & (bins['d_loc'] <= depth_intervals[i][j+1])]
        temp_total = len(temp_bins.be_conc) 
        frac[i][j] = int(temp_total)/int(total)

# Find mass fraction of kaolinte in each depth interval
start = int(crn_in[1][20])+int(crn_in[1][21])
end = int(crn_in[1][20])

for i in range(0,len(time_unique)):
  # Read in the data
    filename='CRUNCH_cells'+str(time_unique[i])+".vtk"
    data  = meshio.read(DataDirectory+filename)
    k_mf = data.cell_data['Mineral_mass_fraction_Kaolinite']
    kmf = k_mf[0][-(start):-(end)]
    for j in range(0,n_depth_intervals):
        flux_frac[i] = flux_frac[i]+((frac[i][j])*kmf[j][0])
    clay_flux[i] = -(flux_frac[i]*flux[i])
dbl_clay_flux_part_mix = clay_flux
# Import the data
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/test_vtk/decrease_base_level/changing_base_level_full_mixing_decrease/'
EpDataDirectory ='/exports/csce/datastore/geos/users/s0933963/test_vtk/decrease_base_level/changing_base_level_decrease_eroded_only/'
#Load all the data
ft_out = pd.read_csv(DataDirectory+'ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )

bins = pd.read_csv(EpDataDirectory+'ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )


# original sed trans
sed_trans_in = pd.read_csv(DataDirectory+'sed_trans_param.stparam',header=None, sep=" ")
# original model run (for base level)
model_run_in = pd.read_csv(DataDirectory+'model_run.param',header=None, sep=" ")
# crn file
crn_in = pd.read_csv(DataDirectory+'CRN_trans_param.CRNparam',header=None, sep=" ")

# erosion rate file
er_in = pd.read_csv(DataDirectory+'erate_hist.param',header=None, sep=" ")
erosion_counter = 0
erosion_age = er_in[erosion_counter][0]
erosion = er_in[erosion_counter+1][0]
# base level file
bl_in = pd.read_csv(DataDirectory+'base_level_hist.param',header=None ,sep=" ")

bl_counter = 0
bl_age = bl_in[bl_counter][0]
bl_old_c = 0
bl_counter = 0


# Set up some parameters
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
time_unique = time_unique
timelabels = time_unique
bins_unique = bins.bn.unique()
bins_unique = np.array(bins_unique)
bins['time'] = bins['time']
div = max(bins_unique)/max(ft_pits)
# Calculate the sediment flux

flux = np.zeros(len(time_unique))
final_node = model_run_in[1][17]
for i in range(0,len(time_unique)):
    # find the new bl
    
    if time_unique[i] > erosion_age:
        erosion_counter = erosion_counter+2
    if time_unique[i] > bl_age:
        diff = time_unique[i]-bl_age
        bl_old_c = bl_counter
        bl_counter = bl_counter+2 
    else:
        diff = 0  

    final_node = final_node-((time_unique[i]-(time_unique[0]*i))-diff)*bl_in[bl_old_c+1][0]-(diff*bl_in[bl_counter+1][0])

    # final_node = np.around(final_node,3)

    bl_old_c = bl_counter
    bl_age = bl_in[bl_counter][0]
    # find the slope
    ds_dist = ft_data[i*pits:i*pits+pits][:,0]
    elev = ft_data[i*pits:i*pits+pits][:,3]
    thick = ft_data[i*pits:i*pits+pits][:,5]
    width = ft_data[i*pits:i*pits+pits][:,1]

    slope = (elev[len(elev)-1]-final_node)/(ds_dist[len(ds_dist)-1]-ds_dist[len(ds_dist)-2])
    denom = 1/(1-slope*slope/(sed_trans_in[1][3]*sed_trans_in[1][3]))
    flux[i] = -sed_trans_in[1][0]*sed_trans_in[1][2]*thick[len(ds_dist)-1]*width[len(ds_dist)-1]*slope*denom
    
# Find number of depth intervals and their type
n_depth_intervals = int(crn_in[1][20])
depth_intervals = np.zeros((len(time_unique),n_depth_intervals+2))
for i in range(0,len(time_unique)):
    thick = ft_data[i*pits:i*pits+pits][:,5]
    depth_intervals[i] = np.linspace(0,thick[len(ds_dist)-1],num=n_depth_intervals+2)



frac = np.zeros((len(time_unique),n_depth_intervals))
flux_frac = np.zeros((len(time_unique)))
clay_flux = np.zeros((len(time_unique)))
# Find proportion of particles in each depth interval
for i in range(0,len(time_unique)):
    for j in range(0,n_depth_intervals):
        
        temp_bins = bins[(bins['time'] == time_unique[i])]
        total = len(temp_bins.be_conc) 
        temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['d_loc'] >= depth_intervals[i][j]) & (bins['d_loc'] <= depth_intervals[i][j+1])]
        temp_total = len(temp_bins.be_conc) 
        frac[i][j] = int(temp_total)/int(total)
       
# Find mass fraction of kaolinte in each depth interval
start = int(crn_in[1][20])+int(crn_in[1][21])
end = int(crn_in[1][20])

for i in range(0,len(time_unique)):
  # Read in the data
    filename='CRUNCH_cells'+str(time_unique[i])+".vtk"
    data  = meshio.read(DataDirectory+filename)
    k_mf = data.cell_data['Mineral_mass_fraction_Kaolinite']
    kmf = k_mf[0][-(start):-(end)]
    for j in range(0,n_depth_intervals):
        flux_frac[i] = flux_frac[i]+((frac[i][j])*kmf[j][0])
    clay_flux[i] = -(flux_frac[i]*flux[i])

dbl_clay_flux_full_mix = clay_flux

# Import the data
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/test_vtk/increase_base_level/changing_base_level/'
EpDataDirectory ='/exports/csce/datastore/geos/users/s0933963/test_vtk/increase_base_level/changing_base_level_eroded_only/'
#Load all the data
ft_out = pd.read_csv(DataDirectory+'ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )

bins = pd.read_csv(EpDataDirectory+'ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )


# original sed trans
sed_trans_in = pd.read_csv(DataDirectory+'sed_trans_param.stparam',header=None, sep=" ")
# original model run (for base level)
model_run_in = pd.read_csv(DataDirectory+'model_run.param',header=None, sep=" ")
# crn file
crn_in = pd.read_csv(DataDirectory+'CRN_trans_param.CRNparam',header=None, sep=" ")

# erosion rate file
er_in = pd.read_csv(DataDirectory+'erate_hist.param',header=None, sep=" ")
erosion_counter = 0
erosion_age = er_in[erosion_counter][0]
erosion = er_in[erosion_counter+1][0]
# base level file
bl_in = pd.read_csv(DataDirectory+'base_level_hist.param',header=None ,sep=" ")

bl_counter = 0
bl_age = bl_in[bl_counter][0]
bl_old_c = 0
bl_counter = 0


# Set up some parameters
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
time_unique = time_unique
timelabels = time_unique
bins_unique = bins.bn.unique()
bins_unique = np.array(bins_unique)
bins['time'] = bins['time']
div = max(bins_unique)/max(ft_pits)
# Calculate the sediment flux

flux = np.zeros(len(time_unique))
final_node = model_run_in[1][17]
for i in range(0,len(time_unique)):
    # find the new bl
    
    if time_unique[i] > erosion_age:
        erosion_counter = erosion_counter+2
    if time_unique[i] > bl_age:
        diff = time_unique[i]-bl_age
        bl_old_c = bl_counter
        bl_counter = bl_counter+2 
    else:
        diff = 0  

    final_node = final_node-((time_unique[i]-(time_unique[0]*i))-diff)*bl_in[bl_old_c+1][0]-(diff*bl_in[bl_counter+1][0])

    # final_node = np.around(final_node,3)

    bl_old_c = bl_counter
    bl_age = bl_in[bl_counter][0]
    # find the slope
    ds_dist = ft_data[i*pits:i*pits+pits][:,0]
    elev = ft_data[i*pits:i*pits+pits][:,3]
    thick = ft_data[i*pits:i*pits+pits][:,5]
    width = ft_data[i*pits:i*pits+pits][:,1]

    slope = (elev[len(elev)-1]-final_node)/(ds_dist[len(ds_dist)-1]-ds_dist[len(ds_dist)-2])
    denom = 1/(1-slope*slope/(sed_trans_in[1][3]*sed_trans_in[1][3]))
    flux[i] = -sed_trans_in[1][0]*sed_trans_in[1][2]*thick[len(ds_dist)-1]*width[len(ds_dist)-1]*slope*denom
  
# Find number of depth intervals and their type
n_depth_intervals = int(crn_in[1][20])
depth_intervals = np.zeros((len(time_unique),n_depth_intervals+2))
for i in range(0,len(time_unique)):
    thick = ft_data[i*pits:i*pits+pits][:,5]
    depth_intervals[i] = np.linspace(0,thick[len(ds_dist)-1],num=n_depth_intervals+2)



frac = np.zeros((len(time_unique),n_depth_intervals))
flux_frac = np.zeros((len(time_unique)))
clay_flux = np.zeros((len(time_unique)))
# Find proportion of particles in each depth interval
for i in range(0,len(time_unique)):
    for j in range(0,n_depth_intervals):
        
        temp_bins = bins[(bins['time'] == time_unique[i])]
        total = len(temp_bins.be_conc) 
        temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['d_loc'] >= depth_intervals[i][j]) & (bins['d_loc'] <= depth_intervals[i][j+1])]
        temp_total = len(temp_bins.be_conc) 
        frac[i][j] = int(temp_total)/int(total)
# Find mass fraction of kaolinte in each depth interval
start = int(crn_in[1][20])+int(crn_in[1][21])
end = int(crn_in[1][20])

for i in range(0,len(time_unique)):
  # Read in the data
    filename='CRUNCH_cells'+str(time_unique[i])+".vtk"
    data  = meshio.read(DataDirectory+filename)
    k_mf = data.cell_data['Mineral_mass_fraction_Kaolinite']
    kmf = k_mf[0][-(start):-(end)]
    for j in range(0,n_depth_intervals):
        flux_frac[i] = flux_frac[i]+((frac[i][j])*kmf[j][0])
    clay_flux[i] = -(flux_frac[i]*flux[i])
ibl_clay_flux_no_mix = clay_flux

# Import the data
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/test_vtk/increase_base_level/changing_base_level_partial_mixing/'
EpDataDirectory ='/exports/csce/datastore/geos/users/s0933963/test_vtk/increase_base_level/changing_base_level_eroded_only/'
#Load all the data
ft_out = pd.read_csv(DataDirectory+'ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )

bins = pd.read_csv(EpDataDirectory+'ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )


# original sed trans
sed_trans_in = pd.read_csv(DataDirectory+'sed_trans_param.stparam',header=None, sep=" ")
# original model run (for base level)
model_run_in = pd.read_csv(DataDirectory+'model_run.param',header=None, sep=" ")
# crn file
crn_in = pd.read_csv(DataDirectory+'CRN_trans_param.CRNparam',header=None, sep=" ")

# erosion rate file
er_in = pd.read_csv(DataDirectory+'erate_hist.param',header=None, sep=" ")
erosion_counter = 0
erosion_age = er_in[erosion_counter][0]
erosion = er_in[erosion_counter+1][0]
# base level file
bl_in = pd.read_csv(DataDirectory+'base_level_hist.param',header=None ,sep=" ")

bl_counter = 0
bl_age = bl_in[bl_counter][0]
bl_old_c = 0
bl_counter = 0


# Set up some parameters
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
time_unique = time_unique
timelabels = time_unique
bins_unique = bins.bn.unique()
bins_unique = np.array(bins_unique)
bins['time'] = bins['time']
div = max(bins_unique)/max(ft_pits)
# Calculate the sediment flux

flux = np.zeros(len(time_unique))
final_node = model_run_in[1][17]
for i in range(0,len(time_unique)):
    # find the new bl
    
    if time_unique[i] > erosion_age:
        erosion_counter = erosion_counter+2
    if time_unique[i] > bl_age:
        diff = time_unique[i]-bl_age
        bl_old_c = bl_counter
        bl_counter = bl_counter+2 
    else:
        diff = 0  

    final_node = final_node-((time_unique[i]-(time_unique[0]*i))-diff)*bl_in[bl_old_c+1][0]-(diff*bl_in[bl_counter+1][0])

    # final_node = np.around(final_node,3)

    bl_old_c = bl_counter
    bl_age = bl_in[bl_counter][0]
    # find the slope
    ds_dist = ft_data[i*pits:i*pits+pits][:,0]
    elev = ft_data[i*pits:i*pits+pits][:,3]
    thick = ft_data[i*pits:i*pits+pits][:,5]
    width = ft_data[i*pits:i*pits+pits][:,1]

    slope = (elev[len(elev)-1]-final_node)/(ds_dist[len(ds_dist)-1]-ds_dist[len(ds_dist)-2])
    denom = 1/(1-slope*slope/(sed_trans_in[1][3]*sed_trans_in[1][3]))
    flux[i] = -sed_trans_in[1][0]*sed_trans_in[1][2]*thick[len(ds_dist)-1]*width[len(ds_dist)-1]*slope*denom
    
# Find number of depth intervals and their type
n_depth_intervals = int(crn_in[1][20])
depth_intervals = np.zeros((len(time_unique),n_depth_intervals+2))
for i in range(0,len(time_unique)):
    thick = ft_data[i*pits:i*pits+pits][:,5]
    depth_intervals[i] = np.linspace(0,thick[len(ds_dist)-1],num=n_depth_intervals+2)



frac = np.zeros((len(time_unique),n_depth_intervals))
flux_frac = np.zeros((len(time_unique)))
clay_flux = np.zeros((len(time_unique)))
# Find proportion of particles in each depth interval
for i in range(0,len(time_unique)):
    for j in range(0,n_depth_intervals):
        
        temp_bins = bins[(bins['time'] == time_unique[i])]
        total = len(temp_bins.be_conc) 
        temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['d_loc'] >= depth_intervals[i][j]) & (bins['d_loc'] <= depth_intervals[i][j+1])]
        temp_total = len(temp_bins.be_conc) 
        frac[i][j] = int(temp_total)/int(total)
       
# Find mass fraction of kaolinte in each depth interval
start = int(crn_in[1][20])+int(crn_in[1][21])
end = int(crn_in[1][20])

for i in range(0,len(time_unique)):
  # Read in the data
    filename='CRUNCH_cells'+str(time_unique[i])+".vtk"
    data  = meshio.read(DataDirectory+filename)
    k_mf = data.cell_data['Mineral_mass_fraction_Kaolinite']
    kmf = k_mf[0][-(start):-(end)]
    for j in range(0,n_depth_intervals):
        flux_frac[i] = flux_frac[i]+((frac[i][j])*kmf[j][0])
    clay_flux[i] = -(flux_frac[i]*flux[i])
ibl_clay_flux_part_mix = clay_flux

# Import the data
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/test_vtk/increase_base_level/changing_base_level_full_mixing/'
EpDataDirectory ='/exports/csce/datastore/geos/users/s0933963/test_vtk/increase_base_level/changing_base_level_eroded_only/'
#Load all the data
ft_out = pd.read_csv(DataDirectory+'ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )

bins = pd.read_csv(EpDataDirectory+'ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )


# original sed trans
sed_trans_in = pd.read_csv(DataDirectory+'sed_trans_param.stparam',header=None, sep=" ")
# original model run (for base level)
model_run_in = pd.read_csv(DataDirectory+'model_run.param',header=None, sep=" ")
# crn file
crn_in = pd.read_csv(DataDirectory+'CRN_trans_param.CRNparam',header=None, sep=" ")

# erosion rate file
er_in = pd.read_csv(DataDirectory+'erate_hist.param',header=None, sep=" ")
erosion_counter = 0
erosion_age = er_in[erosion_counter][0]
erosion = er_in[erosion_counter+1][0]
# base level file
bl_in = pd.read_csv(DataDirectory+'base_level_hist.param',header=None ,sep=" ")

bl_counter = 0
bl_age = bl_in[bl_counter][0]
bl_old_c = 0
bl_counter = 0


# Set up some parameters
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
time_unique = time_unique
timelabels = time_unique
bins_unique = bins.bn.unique()
bins_unique = np.array(bins_unique)
bins['time'] = bins['time']
div = max(bins_unique)/max(ft_pits)
# Calculate the sediment flux

flux = np.zeros(len(time_unique))
final_node = model_run_in[1][17]
for i in range(0,len(time_unique)):
    # find the new bl
    
    if time_unique[i] > erosion_age:
        erosion_counter = erosion_counter+2
    if time_unique[i] > bl_age:
        diff = time_unique[i]-bl_age
        bl_old_c = bl_counter
        bl_counter = bl_counter+2 
    else:
        diff = 0  

    final_node = final_node-((time_unique[i]-(time_unique[0]*i))-diff)*bl_in[bl_old_c+1][0]-(diff*bl_in[bl_counter+1][0])

    # final_node = np.around(final_node,3)

    bl_old_c = bl_counter
    bl_age = bl_in[bl_counter][0]
    # find the slope
    ds_dist = ft_data[i*pits:i*pits+pits][:,0]
    elev = ft_data[i*pits:i*pits+pits][:,3]
    thick = ft_data[i*pits:i*pits+pits][:,5]
    width = ft_data[i*pits:i*pits+pits][:,1]

    slope = (elev[len(elev)-1]-final_node)/(ds_dist[len(ds_dist)-1]-ds_dist[len(ds_dist)-2])
    denom = 1/(1-slope*slope/(sed_trans_in[1][3]*sed_trans_in[1][3]))
    flux[i] = -sed_trans_in[1][0]*sed_trans_in[1][2]*thick[len(ds_dist)-1]*width[len(ds_dist)-1]*slope*denom
    
# Find number of depth intervals and their type
n_depth_intervals = int(crn_in[1][20])
depth_intervals = np.zeros((len(time_unique),n_depth_intervals+2))
for i in range(0,len(time_unique)):
    thick = ft_data[i*pits:i*pits+pits][:,5]
    depth_intervals[i] = np.linspace(0,thick[len(ds_dist)-1],num=n_depth_intervals+2)



frac = np.zeros((len(time_unique),n_depth_intervals))
flux_frac = np.zeros((len(time_unique)))
clay_flux = np.zeros((len(time_unique)))
# Find proportion of particles in each depth interval
for i in range(0,len(time_unique)):
    for j in range(0,n_depth_intervals):
        
        temp_bins = bins[(bins['time'] == time_unique[i])]
        total = len(temp_bins.be_conc) 
        temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['d_loc'] >= depth_intervals[i][j]) & (bins['d_loc'] <= depth_intervals[i][j+1])]
        temp_total = len(temp_bins.be_conc) 
        frac[i][j] = int(temp_total)/int(total)
       
# Find mass fraction of kaolinte in each depth interval
start = int(crn_in[1][20])+int(crn_in[1][21])
end = int(crn_in[1][20])

for i in range(0,len(time_unique)):
  # Read in the data
    filename='CRUNCH_cells'+str(time_unique[i])+".vtk"
    data  = meshio.read(DataDirectory+filename)
    k_mf = data.cell_data['Mineral_mass_fraction_Kaolinite']
    kmf = k_mf[0][-(start):-(end)]
    for j in range(0,n_depth_intervals):
        flux_frac[i] = flux_frac[i]+((frac[i][j])*kmf[j][0])
    clay_flux[i] = -(flux_frac[i]*flux[i])
ibl_clay_flux_full_mix = clay_flux
# print(ss_clay_flux_no_mix)
# print(ss_clay_flux_part_mix)
# print(ss_clay_flux_full_mix)

# print(dbl_clay_flux_no_mix)
# print(dbl_clay_flux_part_mix)
# print(dbl_clay_flux_full_mix)

# print(ibl_clay_flux_no_mix)
# print(ibl_clay_flux_full_mix)

fig = plt.figure(figsize =(15,5))
ax1 = plt.subplot(1,3,1)
x_min = 0.2
x_max = 0.7
ax1.scatter(time_unique,ss_clay_flux_no_mix,c='k',label='No Mixing')
ax1.scatter(time_unique,ss_clay_flux_part_mix,marker='^',c='k',label='Partial Mixing')
ax1.scatter(time_unique,ss_clay_flux_full_mix,marker='x',c='k',label='Full Mixing')
ax1.set_ylim(x_min,x_max)
ax1.legend(loc='lower left')
ax1.set_title('Steady State')
ax2 = plt.subplot(1,3,2)
ax2.scatter(time_unique,dbl_clay_flux_no_mix,c='blue',label='No Mixing')
ax2.scatter(time_unique,dbl_clay_flux_part_mix,marker='^',c='blue',label='Partial Mixing')
ax2.scatter(time_unique,dbl_clay_flux_full_mix,marker='x',c='blue',label='Full Mixing')
ax2.set_ylim(x_min,x_max)
ax2.set_title('Decreasing Erosion')
ax2.legend(loc='lower left')
ax3 = plt.subplot(1,3,3)
ax3.scatter(time_unique,ibl_clay_flux_no_mix,c='red',label='No Mixing')
ax3.scatter(time_unique,ibl_clay_flux_part_mix,marker='^',c='red',label='Partial Mixing')
ax3.scatter(time_unique,ibl_clay_flux_full_mix,marker='x',c='red',label='Full Mixing')
ax3.set_ylim(x_min,x_max)
ax3.legend(loc='lower left')
ax3.set_title('Increasing Erosion')
ax =fig.add_subplot(1,1,1,frameon=False)
ax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
ax.set_ylabel('Clay Flux (Kg $a^{-1}$)',fontsize=18)
    
ax.set_xlabel('Time (years)',fontsize=18)

plt.savefig(DataDirectory+'clay_flux_inheritance.png', dpi=200)
# plt.show()   
