#Script for setting up a series of runs with varying parameter files
#Currently only for mixing model so ignore the crunch infileno crunc infile
import numpy as np
import subprocess
import os
import shutil
from decimal import Decimal
#This assumes that the directory maker sits in a folder one up from the one containing the master param files
root=os.getcwd()
#Specify number of runs
n_runs = 6
#Change the erosion rate or mixing velocity
#Mixing Velocity limits
min_vel = 0.0
max_vel = 0.006
#Erosion rate limits
min_e = 0.0
max_e = 0.0
#Create the arrays to populate
steps = (max_vel-min_vel)/n_runs
mix_vel =np.arange(min_vel,max_vel,steps)
#print(mix_vel)
#steps = (max_e-min_e)/n_runs
#e =np.arange(min_e,max_e,steps)
#print(e)

#These contain the links to the master param files, if parameters need to be varied then this needs to be done by writing a new param file via a loop as below. Replacing specific parts of a text file would make this smoother but this looks tricksy.

#CRM parameter file
m_CRN_fname = root + '/pinedale/CRN_trans_param.CRNparam'
#Flowtube parameter file
m_ftd_fname = root + '/pinedale/ft_details.param'
#Model run parameter file
m_mrn_fname = root + '/pinedale/model_run.param'
#Soil profile parameter file
m_prf_fname = root + '/pinedale/profile.sm'
#Sediment transport paramter file
m_st_fname = root + '/pinedale/sed_trans_param.stparam'
#Particle data parameter file
m_pd_fname = root + '/pinedale/VolumeParticleData.in'

#Here we loop through and create new folders containing the param files which can then be put into the mixing model. Currently the CRN and Model run param files are writted not copied allowing paramters to be varied in them

for i in range(1,n_runs+1):

    #Create a folder to populate then navigating to it plus giving it a helpful name.
    runname = '/pinedale_' + 'mixing_' + str(mix_vel[i-1])
    #To get around decimal points in the file naming
    run_name = runname.replace('.','_')
    dirname = root+run_name
    #print(dirname)
    os.mkdir(dirname)
    os.chdir(dirname)

    r_CRN_fname = 'CRN_trans_param.CRNparam'
    file = open('%s' % r_CRN_fname, 'w')
    file.write('start_depth: ' + str(1.4) + '\n')
    file.write('vert_mix_vel: ' + str(mix_vel[i-1]) + '\n')
    file.write('horiz_mix_vel: ' + str(0.0) + '\n')
    file.write('Omega: ' + str(1.0) + '\n')
    file.write('part_conc: ' + str(0.5) + '\n')
    file.write('CRN_muon_param_switch: ' + str(2) + '\n')
    file.write('single_scaling: ' + str(5.5) + '\n')
    file.write('C_10Be_initial: ' + str(20000.0) + '\n')
    file.write('C_f10Be_initial: ' + str(0.0) + '\n')
    file.write('C_26Al_initial: ' + str(0.0) + '\n')
    file.write('C_36Cl_initial: ' + str(0.0) + '\n')
    file.write('C_14C_initial: ' + str(0.0) + '\n')
    file.write('C_21Ne_initial: ' + str(0.0) + '\n')
    file.write('C_3He_initial: ' + str(0.0) + '\n')
    file.write('M_supply_surface: ' + str(0.0) + '\n')
    file.write('k_f10Be: ' + str(5) + '\n')
    file.write('deltad: ' + str(0.0001) + '\n')
    file.write('k2_f10Be: ' + str(0.001) + '\n')
    file.write('chi_f10Be: ' + str(0.7) + '\n')
    file.write('n_PDZ_intervals: ' + str(5) + '\n')
    file.write('n_CAZ_intervals: ' + str(10) + '\n')
    file.write('lat: ' + str(42) + '\n')
    file.write('lon: ' + str(109) + '\n')
    file.write('site_elev: ' + str(2298) + '\n')
    file.write('Fsp: ' + str(0.98) + '\n')
    file.close


    r_ftd_fname = 'ft_details.param'
    shutil.copy(m_ftd_fname,r_ftd_fname)

    r_mrn_fname = 'model_run.param'
    file = open('%s' % r_mrn_fname, 'w')
    file.write('flux_switch: ' + str(1) + '\n')
    file.write('prod_switch: ' + str(3) + '\n')
    file.write('flux_us: ' + str(0) + '\n')
    file.write('dt: ' + str(10) + '\n')
    file.write('CRN_switch: ' + str(3) + '\n')
    file.write('end_time: ' + str(19000) + '\n')
    file.write('surf_erate: -' + str(0.0000025) + '\n')
    file.write('particle_printing_interval: ' + str(19000) + '\n')
    file.write('eroded_catch_window: ' + str(500) + '\n')
    file.write('max_age: ' + str(19000) + '\n')
    file.write('n_spacings: ' + str(500) + '\n')
    file.write('particle_insert_interval: ' + str(100) + '\n')
    file.write('weathering_time_interval: ' + str(998) + '\n')
    file.write('ref_frame_switch: ' + str(0) + '\n')
    file.write('SS_flux: ' + str(0) + '\n')
    file.write('lower_boundary_condition: ' + str(1) + '\n')
    file.close



    r_prf_fname = 'profile.sm'
    shutil.copy(m_prf_fname,r_prf_fname)

    r_st_fname = 'sed_trans_param.stparam'
    shutil.copy(m_st_fname,r_st_fname)

    r_pd_fname ='VolumeParticleData.in'
    shutil.copy(m_pd_fname,r_pd_fname)
    #Change directory back to the root directory for start of new loop
    os.chdir(root)
