import numpy as np
import pandas as pd

#Read the flowtube file
flowtube_file = np.genfromtxt("/exports/csce/datastore/geos/users/s0933963/github/ModelTesting/flowtube_testing/tv_flowtube_details.csv", delimiter =',', skip_header=0, names=['distance','center_x','center_y','center_z','bdry1_x','bdry1_y','brdy2_x','brdy2_y','width','area_quad','area_other'] )
print('loaded')
#Read the pit data file
#pit_data = np.loadtxt("/Users/louis/Documents/GitHub/ModelTesting/flowtube_testing/fta_sites.txt",delimiter=',',skiprows=1,usecols=(0,1,3))
pit_data = np.loadtxt("/exports/csce/datastore/geos/users/s0933963/github/ModelTesting/flowtube_testing/tv_sites_updated.txt",delimiter=',',usecols=(0,1,2))
#pit_data = np.loadtxt("/Users/louis/Documents/GitHub/ModelTesting/flowtube_testing/pomd_sites.txt",delimiter=',',skiprows=1,usecols=(0,1,3))
#Sort the pit data file with highest elevation first
pit_data[::-1].sort(axis=0)
#Number of pits
n_pits = len(pit_data)
#Number of bins, this is so we can create a number of small bins (for th pits) along with larger bins encompassing the flowtube in general.
n_bins = n_pits*2+1

#Now loop through the files adding together values until you reach a pit boundary the stop to make the pit
pit_counter = 0
bin_counter = 1
#print(pit_data)

#set up the flowtube out file array making the first row details from the flowtube file
flowtube = np.zeros((n_bins,5),dtype=np.float)
flowtube[0][0] = 0.001
flowtube[0][1] = flowtube_file[0]['width']
flowtube[0][2] = flowtube_file[0]['area_quad']
flowtube[0][3] = flowtube_file[0]['center_z']
flowtube[0][4] = 0.1
#print(flowtube)
#print((flowtube_file['center_z'][0]))
#print(pit_data[pit_counter][2]-0.3)
for i in range(1,len(flowtube_file)):
    if (flowtube_file['center_z'][i]-0.1) > pit_data[pit_counter][2]:
        #Add the distance
        flowtube[bin_counter][0] = (flowtube_file[i]['distance']-flowtube_file[0]['distance'])
        #Record the width
        flowtube[bin_counter][1] = flowtube_file[i]['width']
        #Add the area
        flowtube[bin_counter][2] = flowtube[bin_counter][2]+(flowtube_file[i]['area_quad'])
        #Record the elevation
        flowtube[bin_counter][3] = flowtube_file[i]['center_z']
        # print(i)
#        ###What to do about interp h?
#       print('done')

    elif (flowtube_file['center_z'][i]) > (pit_data[pit_counter][2]-0.1):
        flowtube[bin_counter+1][0] = (flowtube_file[i]['distance']-flowtube_file[0]['distance'])
        #Record the width
        flowtube[bin_counter+1][1] = flowtube_file[i]['width']
        #Add the area
        flowtube[bin_counter+1][2] = flowtube[bin_counter+1][2]+(flowtube_file[i]['area_quad'])
        #Record the elevation
        flowtube[bin_counter+1][3] = flowtube_file[i]['center_z']
        # print(i)
#        print('meesa done master anakin')
    elif pit_counter+2 <= n_pits:
         pit_counter = pit_counter+1
         bin_counter = bin_counter+2
         flowtube[bin_counter][0] = (flowtube_file[i]['distance']-flowtube_file[0]['distance'])
        #Record the width
         flowtube[bin_counter][1] = flowtube_file[i]['width']
        #Add the area
         flowtube[bin_counter][2] = flowtube[bin_counter][2]+(flowtube_file[i]['area_quad'])
        #Record the elevation
         flowtube[bin_counter][3] = flowtube_file[i]['center_z']
         # print(i)



         print(pit_counter)
#         print(bin_counter)


np.savetxt("tv_flowtube_file.csv", flowtube, delimiter=" ",header='ds_dist,width,Area,elev,interp_h')











