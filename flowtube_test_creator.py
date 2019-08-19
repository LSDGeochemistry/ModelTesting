

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

#print(dem.GetMetadata)
#Convert the raster
raster = np.array(dem.GetRasterBand(1).ReadAsArray())
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
#Now create a new array to make things easier, saves the distance downslope with the x, y, and z coordinates(z coordinates not ciurrently added)
ft_center = np.zeros((len(center_point_vertices),4),dtype=np.float)
for i in range (1,len(center_point_vertices)):
   ft_center[i][0] = np.sqrt((center_point_vertices[i][0][0]-center_point_vertices[i][1][0])**2+(center_point_vertices[i][0][1]-center_point_vertices[i][1][1])**2)+ft_center[i-1][0]
   ft_center[i][1] = (center_point_vertices[i][0][0]+center_point_vertices[i][1][0])/2
   ft_center[i][2] = (center_point_vertices[i][0][1]+center_point_vertices[i][1][1])/2
#print(ft_center)
#Now find the flowlines for the boundary of the flowtube
#Left most boundary
boundary_1 = [[50,55]]
boundary_1_line = plt.streamplot(xv,yv,gradx,grady,start_points=boundary_1,linewidth=0.4,density=10).lines
boundary_1_vertices = boundary_1_line.get_segments()
ft_left = np.zeros((len(boundary_1_vertices),4),dtype=np.float)
for i in range (1,len(boundary_1_vertices)):
   ft_left[i][0] = np.sqrt((boundary_1_vertices[i][0][0]-boundary_1_vertices[i][1][0])**2+(boundary_1_vertices[i][0][1]-boundary_1_vertices[i][1][1])**2)+ft_left[i-1][0]
   ft_left[i][1] = (boundary_1_vertices[i][0][0]+boundary_1_vertices[i][1][0])/2
   ft_left[i][2] = (boundary_1_vertices[i][0][1]+boundary_1_vertices[i][1][1])/2
#print(ft_left)
#Right most boundary
boundary_2 = [[50,45]]
boundary_2_line = plt.streamplot(xv,yv,gradx,grady,start_points=boundary_2,linewidth=0.4,density=10).lines
boundary_2_vertices = boundary_2_line.get_segments()
ft_right = np.zeros((len(boundary_2_vertices),4),dtype=np.float)
for i in range (1,len(boundary_2_vertices)):
   ft_right[i][0] = np.sqrt((boundary_2_vertices[i][0][0]-boundary_2_vertices[i][1][0])**2+(boundary_2_vertices[i][0][1]-boundary_2_vertices[i][1][1])**2)+ft_right[i-1][0]
   ft_right[i][1] = (boundary_2_vertices[i][0][0]+boundary_2_vertices[i][1][0])/2
   ft_right[i][2] = (boundary_2_vertices[i][0][1]+boundary_2_vertices[i][1][1])/2
#print(ft_right)

#Now need to get the data from the flowtube








##seedpoint = np.array([[50,50,50],[46,50,54]])
#seedpoint = [[50,45],[50,50],[50,55]]
#fig = plt.figure()
#ax=fig.add_subplot(1,1,1)
#ax.matshow(raster)
#ax.streamplot(xv,yv,gradx,grady,start_points=seedpoint,linewidth=0.4,density=10)
#
#
#ax.set_xlim(20,60)
#ax.set_ylim(20,60)
#test_list = ax.streamplot(xv,yv,gradx,grady,start_points=seedpoint,linewidth=0.4,density=10).lines
##print(test_list)
#test = test_list.get_segments()
##print(test)
##plt.quiver(gradx,grady, scale=30)


#plt.savefig('test.png')
#plt.matshow(raster)
#
#plt.savefig('test_raster.png')
#plt.close()
#
#
#
#print('done')