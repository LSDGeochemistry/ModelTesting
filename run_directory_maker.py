#Script for setting up a series of runs with varying parameter files
#Currently only for mixing model so ignore the crunch infile

import numpy as np
import subprocess
import os
import shutil

root=os.getcwd()
#Sepcify number of runs
n_runs = 11

#CRM parameter file
m_CRN_fname = root + '/master_params/CRN_trans_param.CRNparam'
#Flowtube parameter file
m_ftd_fname = root + '/master_params/ft_details.param'
#Model run parameter file
m_mrn_fname = root + '/master_params/model_run.param'
#Soil profile parameter file
m_prf_fname = root + '/master_params/profile.sm'
#Sediment transport paramter file
m_st_fname = root + '/master_params/sed_trans_param.stparam'
#Particle data parameter file
m_pd_fname = root + '/master_params/VolumeParticleData.in'

for i in range(1,n_runs+1):
    run_name = '/run' + str(i)
    dirname = root+run_name
    os.mkdir(dirname)
    
    r_CRN_fname = dirname+run_name+'.CRN_trans_param.CRNparam'
    shutil.copy(m_CRN_fname,r_CRN_fname)
    
    r_ftd_fname = dirname+run_name+'.ft_details.param'
    shutil.copy(m_ftd_fname,r_ftd_fname)
    
    r_mrn_fname = dirname+run_name+'.model_run.param'
    shutil.copy(m_mrn_fname,r_mrn_fname)
    
    r_prf_fname = dirname+run_name+'.profile.sm'
    shutil.copy(m_prf_fname,r_prf_fname)

    r_st_fname = dirname+run_name+'.sed_trans_param.stparam'
    shutil.copy(m_st_fname,r_st_fname)
    
    r_pd_name = dirname+run_name+'.VolumeParticleData.in'
    shutil.copy(m_pd_fname,r_pd_fname)