import numpy as np
import pandas as pd

#Read the flowtube file
flowtube_file = pd.read_csv("C:/Workspace/github/ModelTesting/flowtube_testing/fta_flowtube_details.csv", names=['distance','center_x','center_y','center_z','bdry1_x','bdry1_y','brdy2_x','brdy2_y','width','area_quad','area_other'] )
print('loaded')
#Read the pit data file
pit_data = np.loadtxt("C:/Workspace/github/ModelTesting/flowtube_testing/fta_sites.txt")

#Number of pits
n_pits = 5
#Number of bins, this is so we can create a number of small bins (for th pits) along with larger bins encompassing the flowtube in general.
n_bins = n_pits*2+1

#Now loop through the files adding together values until you reach a pit boundary the stop to make the pit
pit_counter = 0
bin_counter = 0
counter = 0

#set up the flowtube out file array
flowtube = np.zeros((n_bins,5),dtype=np.float)

for i in range(len(flowtube_file)):
    if flowtube_file['center_z'][i] < pit_data[pit_counter][2]
        
    


