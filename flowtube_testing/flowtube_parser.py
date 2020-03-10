import numpy as np
import pandas as pd

#Read the flowtube file
flowtube_file = np.genfromtxt("C:/Workspace/github/ModelTesting/flowtube_testing/fta_flowtube_details.csv", delimiter =',', skip_header=0, names=['distance','center_x','center_y','center_z','bdry1_x','bdry1_y','brdy2_x','brdy2_y','width','area_quad','area_other'] )
print('loaded')
#Read the pit data file
pit_data = np.loadtxt("C:/Workspace/github/ModelTesting/flowtube_testing/fta_sites.txt",delimiter=',',skiprows=1,usecols=(0,1,3))
#Sort the pit data file with highest elevation first
pit_data[::-1].sort(axis=0)
#Number of pits
n_pits = 10
#Number of bins, this is so we can create a number of small bins (for th pits) along with larger bins encompassing the flowtube in general.
n_bins = n_pits*2+1

#Now loop through the files adding together values until you reach a pit boundary the stop to make the pit
pit_counter = 0
bin_counter = 1
counter = 0

#set up the flowtube out file array
flowtube = np.zeros((n_bins,5),dtype=np.float)
flowtube[0][0] = flowtube_file[0]['distance']
flowtube[0][1] = flowtube_file[0]['width']
flowtube[0][2] = flowtube_file[0]['area_quad']
flowtube[0][3] = flowtube_file[0]['center_z']
flowtube[0][4] = 0.1
#print((flowtube_file['center_z'][0]+0.3))
#print(pit_data[pit_counter][2])
for i in range(1,len(flowtube_file)):
    if (flowtube_file['center_z'][i]+0.3) > pit_data[pit_counter][2]: 
        #Add the distance
        flowtube[bin_counter][0] = flowtube[bin_counter][0]+(flowtube_file[i]['distance']-flowtube_file[0]['distance'])
        #Record the width
        flowtube[bin_counter][1] = flowtube_file[i]['width']
        #Add the area
        flowtube[bin_counter][2] = flowtube[bin_counter][2]+(flowtube_file[i]['area_quad'])
        #Record the elevation
        flowtube[bin_counter][3] = flowtube_file[i]['center_z']
        ###What to do about interp h?
        #print('done')
    elif (flowtube_file['center_z'][i]-0.3) > pit_data[pit_counter][2] :
        
print(flowtube)

        
        
        
        
    


