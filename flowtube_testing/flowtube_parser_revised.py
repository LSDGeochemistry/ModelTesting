import numpy as np
import pandas as pd

#Read the flowtube file
flowtube_file = np.genfromtxt("/exports/csce/datastore/geos/users/s0933963/github/ModelTesting/flowtube_testing/brc_flowtube_details_test.csv", delimiter =',', skip_header=0, names=['distance','center_x','center_y','center_z','bdry1_x','bdry1_y','brdy2_x','brdy2_y','width','area_quad','area_other'] )
# print('loaded')
# print(flowtube_file)
#Read the pit data file
# pit_data = np.loadtxt("/Users/louis/Documents/GitHub/ModelTesting/flowtube_testing/fta_sites.txt",delimiter=',',skiprows=1,usecols=(0,1,3))
pit_data = np.loadtxt("/exports/csce/datastore/geos/users/s0933963/github/ModelTesting/flowtube_testing/brc_sites.txt",delimiter=',',skiprows=1,usecols=(0,1,3,4))
#pit_data = np.loadtxt("/Users/louis/Documents/GitHub/ModelTesting/flowtube_testing/pomd_sites.txt",delimiter=',',skiprows=1,usecols=(0,1,3))
#Sort the pit data file with highest elevation first
# pit_data[::-1].sort(axis=0)
pit_data = pit_data[pit_data[:, 2].argsort()]
pit_data = pit_data[::-1]
# print(pit_data)
#Number of pits
n_pits = len(pit_data)
#Number of bins, this is so we can create a number of small bins (for th pits) along with larger bins encompassing the flowtube in general.

# Number of metres
sep = 0.5
temp_sep = 0
flowtube_temp_area = 0
length = int((max(flowtube_file['distance'])-min(flowtube_file['distance'])+1)/sep)
length_index = 1

#Now loop through the files adding together values until you reach a pit boundary the stop to make the pit
pit_counter = 1

#print(pit_data)

#set up the flowtube out file array making the first row details from the flowtube file
flowtube = np.zeros((length,5),dtype=np.float)
flowtube[0][0] = 0.0
flowtube[0][1] = flowtube_file[0]['width']
flowtube[0][2] = flowtube_file[0]['area_quad']
flowtube[0][3] = flowtube_file[0]['center_z']
flowtube[0][4] = pit_data[0][3]

# print(flowtube)

for i in range(1,len(flowtube_file)):
    # print(temp_sep)
    if temp_sep < sep:
        #Add the area
        flowtube_temp_area = flowtube_temp_area+flowtube_file[i]['area_quad']

        temp_sep = temp_sep+(flowtube_file[i]['distance']-flowtube_file[i-1]['distance'])
    if temp_sep >= sep:
        frac = (temp_sep-sep)/flowtube_file[i]['distance']
        flowtube[length_index][0] = flowtube[length_index-1][0]+sep
        flowtube[length_index][1] = (flowtube_file[i-1]['width']+(flowtube_file[i]['width']*frac))/(1+frac)
        flowtube[length_index][2] = flowtube_temp_area+(flowtube_file[i]['area_quad']*frac)
        flowtube[length_index][3] = (flowtube_file[i-1]['center_z']+(flowtube_file[i]['center_z']*frac))/(1+frac)
        flowtube[length_index][4] = 0.1
        if flowtube[length_index][3] < pit_data[pit_counter][2]:
            flowtube[length_index][4] = pit_data[pit_counter][3]
            if pit_counter < len(pit_data)-1:
                pit_counter = pit_counter+1
            else:
                pit_counter = pit_counter
        else:
            flowtube[length_index][4] = pit_data[pit_counter-1][3]
        temp_sep = 0+(temp_sep-sep)
        flowtube_temp_area = 0+(1-frac)*flowtube_file[i]['area_quad']
        length_index = length_index+1


# print(flowtube)

    


#         print(pit_counter)
#         print(bin_counter)


np.savetxt("brc_test_out.csv", flowtube, delimiter=",",header='ds_dist,width,Area,elev,interp_h')