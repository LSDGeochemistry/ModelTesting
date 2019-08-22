

import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal

###Section containing user defined parameters
#Ehe DEM resolution (m)
dem_r = 10
#The pathway to the DEM
fname = "R:/feather_river_mixing_paper/dem/pomd_out.tif"
#Open the DEM using GDAL
dem = gdal.Open(fname)
print('loaded dem')
#Load the soil pit data, atm is just a placeholder array
pits = [[50,50],[48,45],[45,35],[40,30]]
#Distance along the flowtube for the starting point
start_width = 1.0
#print(dem.GetMetadata)
#Convert the raster
raster = np.array(dem.GetRasterBand(1).ReadAsArray())
####Add this in later when not dealing with LIDAR
#Intrpolate the raster for higher definition
#Needs two variables, the resolution of the loaded raster and the desitreed resolution
dem_r = 1
dem_desired = 1
###Use scipy griddata function here, add later though
#Get the gradient of the raster in both x and y directions, multiplying value by negative one to ensure flow in right direction
gradx = np.gradient(raster, axis = 1)*-1
grady = np.gradient(raster, axis = 0)*-1
#Find the shape of each raster and save it to make a grid
raster_shape = np.shape(gradx)
np.asarray(raster_shape)
nx,ny=[raster_shape[1],raster_shape[0]]
#Set up the paramters to make the grid
x = np.linspace(0, nx, nx)
y = np.linspace(0, ny, ny)
xv, yv = np.meshgrid(x, y)
#Set the start point for the centreline on the grid
center_point = [[50,50]]
#Now find the centerline
center_point_line = plt.streamplot(xv,yv,gradx,grady,start_points=center_point,linewidth=0.4,density=10).lines
#Create a temp list to store the data from the centerpoint, this creates a list of arraysfof reach point
center_point_vertices = center_point_line.get_segments()
#Now create a new array to make things easier, saves the distance downslope with the x, y, and z coordinates(z coordinates not currently added)
ft_center = np.zeros((len(center_point_vertices),4),dtype=np.float)
#Now go throug the temp vertices file and extract the values [distance,x,y,z(not implemented yet)]
for i in range (1,len(center_point_vertices)):
   ft_center[i][0] = np.sqrt((center_point_vertices[i][0][0]-center_point_vertices[i][1][0])**2+(center_point_vertices[i][0][1]-center_point_vertices[i][1][1])**2)+ft_center[i-1][0]
   ft_center[i][1] = (center_point_vertices[i][0][0]+center_point_vertices[i][1][0])/2
   ft_center[i][2] = (center_point_vertices[i][0][1]+center_point_vertices[i][1][1])/2
   #Find the index of the starting point
   if center_point_vertices[i][0][0] == center_point[0][0]:
        center_index = i
#Now we have the flowtube center file containing the useful data
#print(ft_center)

#Now find the flowlines for the boundary of the flowtube
#Boundary 1, start by moving along the contour line for a given amount
contour_1 = plt.streamplot(xv,yv,grady,-(gradx),start_points=center_point,linewidth=0.4,density=10).lines
contour_1_vertices = contour_1.get_segments()
contour_1_data = np.zeros((len(contour_1_vertices),4),dtype=np.float)
#Now loop through to get the prescribed distance away
for i in range (1,len(contour_1_vertices)):
   contour_1_data[i][0] = np.sqrt((contour_1_vertices[i][0][0]-contour_1_vertices[i][1][0])**2+(contour_1_vertices[i][0][1]-contour_1_vertices[i][1][1])**2)+contour_1_data[i-1][0]
   contour_1_data[i][1] = (contour_1_vertices[i][0][0]+contour_1_vertices[i][1][0])/2
   contour_1_data[i][2] = (contour_1_vertices[i][0][1]+contour_1_vertices[i][1][1])/2
   #find the closest indext for the x value
   if contour_1_vertices[i][0][0] == center_point[0][0]:
        center_index_x = i
#Now move along the flowtube contour to the prescribed distance along to get the values within the max starting width defined earlier        
for i in range (center_index_x,len(contour_1_data)):
        print('found')
        bdry1_width = []
        for j in range (0,(len(contour_1_data)-i-1)):
            if contour_1_data[j+i][0]-contour_1_data[i][0] <= start_width:
                    bdry1_width.append(contour_1_data[i+j])
                   
        break
#The start point for this boundary is taken from the final row of values from the bdry1_width list       
bdry1_start = [[bdry1_width[len(bdry1_width)-1][1],bdry1_width[len(bdry1_width)-1][2]]]
#Print the x y coordinates of this point to make sure they're reasonable
print(bdry1_start)
#Now feed these boundary points into the streamp[lot fucntion to get the flowtube                    
boundary_1_line = plt.streamplot(xv,yv,gradx,grady,start_points=bdry1_start,linewidth=0.4,density=10).lines
boundary_1_vertices = boundary_1_line.get_segments()
bdry1 = np.zeros((len(boundary_1_vertices),4),dtype=np.float)
for i in range (1,len(boundary_1_vertices)):
   bdry1[i][0] = np.sqrt((boundary_1_vertices[i][0][0]-boundary_1_vertices[i][1][0])**2+(boundary_1_vertices[i][0][1]-boundary_1_vertices[i][1][1])**2)+bdry1[i-1][0]
   bdry1[i][1] = (boundary_1_vertices[i][0][0]+boundary_1_vertices[i][1][0])/2
   bdry1[i][2] = (boundary_1_vertices[i][0][1]+boundary_1_vertices[i][1][1])/2
   if boundary_1_vertices[i][0][0] == bdry1_start[0][0]:
        boundary_index_1 = i
    
##Right most boundary
contour_2 = plt.streamplot(xv,yv,-(grady),gradx,start_points=center_point,linewidth=0.4,density=10).lines
contour_2_vertices = contour_2.get_segments()
contour_2_data = np.zeros((len(contour_2_vertices),4),dtype=np.float)
#Now loop through to get the prescribed distance away
for i in range (1,len(contour_1_vertices)):
   contour_2_data[i][0] = np.sqrt((contour_2_vertices[i][0][0]-contour_2_vertices[i][1][0])**2+(contour_2_vertices[i][0][1]-contour_2_vertices[i][1][1])**2)+contour_2_data[i-1][0]
   contour_2_data[i][1] = (contour_2_vertices[i][0][0]+contour_2_vertices[i][1][0])/2
   contour_2_data[i][2] = (contour_2_vertices[i][0][1]+contour_2_vertices[i][1][1])/2
   #find the closest indext for the x value
   if contour_2_vertices[i][0][0] == center_point[0][0]:
        center_index_x = i
#Now move along the flowtube contour to the prescribed distance along to get the values within the max starting width defined earlier        
for i in range (center_index_x,len(contour_2_data)):
        print('found')
        bdry2_width = []
        for j in range (0,(len(contour_2_data)-i-1)):
            if contour_2_data[j+i][0]-contour_2_data[i][0] <= start_width:
                    bdry2_width.append(contour_2_data[i+j])
                   
        break
#The start point for this boundary is taken from the final row of values from the bdry1_width list       
bdry2_start = [[bdry2_width[len(bdry2_width)-1][1],bdry2_width[len(bdry2_width)-1][2]]]
#Print the x y coordinates of this point to make sure they're reasonable
print(bdry2_start)
#Now feed these boundary points into the streamplot fucntion to get the flowtube                    
boundary_2_line = plt.streamplot(xv,yv,gradx,grady,start_points=bdry2_start,linewidth=0.4,density=10).lines
boundary_2_vertices = boundary_2_line.get_segments()

bdry2 = np.zeros((len(boundary_2_vertices),4),dtype=np.float)
for i in range (1,len(boundary_2_vertices)):
   bdry2[i][0] = np.sqrt((boundary_2_vertices[i][0][0]-boundary_2_vertices[i][1][0])**2+(boundary_2_vertices[i][0][1]-boundary_2_vertices[i][1][1])**2)+bdry2[i-1][0]
   bdry2[i][1] = (boundary_2_vertices[i][0][0]+boundary_2_vertices[i][1][0])/2
   bdry2[i][2] = (boundary_2_vertices[i][0][1]+boundary_2_vertices[i][1][1])/2
   if boundary_2_vertices[i][0][0] == bdry2_start[0][0]:
        boundary_index_2 = i


###Now cut the flowtube arrays so they just go from the start points rather they go from the defined start points
ft_center = np.delete(ft_center,slice(0,center_index),axis=0)
bdry1 = np.delete(bdry1,slice(0,boundary_index_1),axis=0)
bdry2 = np.delete(bdry2,slice(0,boundary_index_2),axis=0)


        

      

#Now need to get the data from the flowtube








###Plot the figure
fig = plt.figure()
ax=fig.add_subplot(1,1,1)
#ax.matshow(raster)
ax.streamplot(xv,yv,gradx,grady,start_points=center_point,linewidth=0.4,density=10)
ax.streamplot(xv,yv,gradx,grady,start_points=bdry1_start,linewidth=0.4,density=10)
ax.streamplot(xv,yv,gradx,grady,start_points=bdry2_start,linewidth=0.4,density=10)

ax.set_xlim(35,55)
ax.set_ylim(20,55)





plt.savefig('test.png')
plt.matshow(raster)

plt.savefig('test_raster.png')
plt.close()



print('done')