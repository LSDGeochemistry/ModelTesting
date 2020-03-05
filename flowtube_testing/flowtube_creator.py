import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal
from scipy import interpolate

###Section containing user defined parameters
#The pathway to the DEM
fname = "C:/Workspace/github/ModelTesting/flowtube_testing/feather_dems/fta.bil"
#Open the DEM using GDAL
dem = gdal.Open(fname)
print('loaded dem')
#Read in the coordinates, needs changed for whatever files being rea
###Depends on the file format
#For POMD
#coord_file = open("R:/feather_river_mixing_paper/dem/pomd_out.tfw","r")
#coord_file = coord_file.read().split('\n')
#coord_file = [float(i) for i in coord_file]
#up_left_e = coord_file[4]
#up_left_n = coord_file[5]
#center_point = [[645391,4389698]]
#For BRC
#up_left_e = 645632.5
#up_left_n = 4390104.5
#center_point = [[645654.5,4390031]]

#For FTA
up_left_e = 645616.5
up_left_n = 4390063.5
center_point = [[645634,4390048]]
#Load the soil pit data and convert to the array coordinates
#Change these accordingly
pits = np.loadtxt("C:/Workspace/github/ModelTesting/flowtube_testing/fta_sites.txt",delimiter=',',skiprows=1,usecols=(0,1,3))

for i in range(0,len(pits)):
    pits[i][0] = pits[i][0]-up_left_e
    pits[i][1] = (pits[i][1]-up_left_n)*-1
pits = np.array(pits)
    
#print(pits)








#Distance along the flowtube for the starting point
start_width = 4.0
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
print(raster_shape)
np.asarray(raster_shape)
nx,ny=[raster_shape[1],raster_shape[0]]
#Set up the paramters to make the grid
x = np.linspace(0, nx, nx)
y = np.linspace(0, ny, ny)
xv, yv = np.meshgrid(x, y)
#Set the start point for the centerline on the grid Move this up to getting file?

#convert the start point
center_point[0][0] = center_point[0][0]-up_left_e
center_point[0][1] = (center_point[0][1]-up_left_n)*-1

print(center_point)
#Now find the centerline
center_point_line = plt.streamplot(xv,yv,gradx,grady,start_points=center_point,linewidth=0.4,density=10).lines
#Create a temp list to store the data from the centerpoint, this creates a list of arraysfof reach point
center_point_vertices = center_point_line.get_segments()
#Now create a new array to make things easier, saves the distance downslope with the x, y, and z coordinates(z coordinates not currently added)
ft_center = np.zeros((len(center_point_vertices),4),dtype=np.float)
raster_temp = np.flipud(raster)

#Now go throug the temp vertices file and extract the values [distance,x,y,z]
for i in range (1,len(center_point_vertices)):
   ft_center[i][0] = np.sqrt((center_point_vertices[i][0][0]-center_point_vertices[i][1][0])**2+(center_point_vertices[i][0][1]-center_point_vertices[i][1][1])**2)+ft_center[i-1][0]
   ft_center[i][1] = (center_point_vertices[i][0][0]+center_point_vertices[i][1][0])/2
   ft_center[i][2] = (center_point_vertices[i][0][1]+center_point_vertices[i][1][1])/2
   elev = interpolate.RectBivariateSpline(y,x, raster_temp); zi = elev(ft_center[i][0], ft_center[i][1])
   ft_center[i][3] = zi
   #Find the index of the starting point
   if center_point_vertices[i][0][0] == center_point[0][0]:
        center_index = i
#Now we have the flowtube center file containing the useful data
#print(ft_center)

#Now find the flowlines for the boundary of the flowtube

###########Left most boundary#############################
#Boundary 1, start by moving along the contour line for a given amount towards y axis (so x = 0)
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
###############################################################
        
#########Right most boundary###################################
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
###############################################################

###Now cut the flowtube arrays so they just go from the start points rather they go from the defined start points
ft_center = np.delete(ft_center,slice(0,center_index-1),axis=0)
bdry1 = np.delete(bdry1,slice(0,boundary_index_1-1),axis=0)
bdry2 = np.delete(bdry2,slice(0,boundary_index_2-1),axis=0)
#Fix it so the bottom of the flowtube is just past the last pit, removes some hassle of manual changing of length etc
ft_center = ft_center[ft_center[:,3]>(min(pits[:,2])-1)]


        

      

#Now need to get the width data from the flowtube
#Retrace the flowtube from one boundary to the other
#Start by running a flowtube from the coordinates of the starting point for boundary number 1
#temp_width = plt.streamplot(xv,yv,-(gradx),grady,start_points=bdry1_start,linewidth=0.4,density=10).lines
#temp_vertices = temp_width.get_segments()
#temp_width = np.zeros((len(temp_vertices),4),dtype=np.float)
#for i in range (1,len(temp_vertices)):
#   temp_width[i][0] = np.sqrt((temp_vertices[i][0][0]-temp_vertices[i][1][0])**2+(temp_vertices[i][0][1]-temp_vertices[i][1][1])**2)+temp_width[i-1][0]
#   temp_width[i][1] = (temp_vertices[i][0][0]+temp_vertices[i][1][0])/2
#   temp_width[i][2] = (temp_vertices[i][0][1]+temp_vertices[i][1][1])/2
#   if temp_vertices[i][0][0] == bdry1_start[0][0]:
#        temp_index = i
#temp_width = np.delete(temp_width,slice(0,temp_index),axis=0)       
#
##Now loop through to get the width at this point
##Some temp variables for the loop
#d_old = 100.0
#d_new = 99.0
#dist = 0.0
#i = 0
#while (d_new < d_old):
#    d_old = d_new
#    i = i+1
#    dx = temp_width[i][1]-bdry2[0][1]
#    dy = temp_width[i][2]-bdry2[0][2]
#    d_new = np.sqrt((dx**2)+(dy**2))
#    ddx = temp_width[i][1]-temp_width[i-1][1]
#    ddy = temp_width[i][2]-temp_width[i-1][2]
#    dist = dist + np.sqrt((ddx**2)+(ddy**2))
    


#Loop through now finding the width at every point along with the area.
#First create an array to accomodate this infromation
flowtube = np.zeros((len(ft_center),11),dtype=np.float)
for i in range(0,len(ft_center)):
#Get the centerline data
        flowtube[i][0] = ft_center[i][0]
        flowtube[i][1] = ft_center[i][1]
        flowtube[i][2] = ft_center[i][2]
        flowtube[i][3] = ft_center[i][3]
#Now for the boundary/width data
        flowtube[i][4] = bdry1[i][1]
        flowtube[i][5] = bdry1[i][2]
        flowtube[i][6] = bdry2[i][1]
        flowtube[i][7] = bdry2[i][2]
        start_point = [[flowtube[i][4],flowtube[i][5]]]
#Now begin a labourious loop to gather data
        temp_width = plt.streamplot(xv,yv,-(gradx),grady,start_points=start_point,linewidth=0.4,density=10).lines
        temp_vertices = temp_width.get_segments()
        temp_width = np.zeros((len(temp_vertices),4),dtype=np.float)
        for k in range (1,len(temp_vertices)):
           temp_width[k][0] = np.sqrt((temp_vertices[k][0][0]-temp_vertices[k][1][0])**2+(temp_vertices[k][0][1]-temp_vertices[k][1][1])**2)+temp_width[k-1][0]
           temp_width[k][1] = (temp_vertices[k][0][0]+temp_vertices[k][1][0])/2
           temp_width[k][2] = (temp_vertices[k][0][1]+temp_vertices[k][1][1])/2
           if temp_vertices[k][0][0] == start_point[0][0]:
                temp_index = k
        temp_width = np.delete(temp_width,slice(0,temp_index-1),axis=0)       

        #Now loop through to get the width at this point
        #Some temp variables for the loop
        d_old = 100.0
        d_new = 99.0
        dist = 0.0
        j = 0
        while (d_new < d_old):
            d_old = d_new
            j = j+1
            dx = temp_width[j][1]-flowtube[i][6]
            dy = temp_width[j][2]-flowtube[i][7]
            d_new = np.sqrt((dx**2)+(dy**2))
            ddx = temp_width[j][1]-temp_width[j-1][1]
            ddy = temp_width[j][2]-temp_width[j-1][2]
            dist = dist + np.sqrt((ddx**2)+(ddy**2))
        flowtube[i][8] = dist
        #Now do the area via a quadrilateral method
        if i != 0:
            dxa = flowtube[i-1][4]-flowtube[i-1][1]
            dya = flowtube[i-1][5]-flowtube[i-1][2]
            a = np.sqrt(dxa**2+dya**2)
            dxb = flowtube[i-1][1]-flowtube[i][1]
            dyb = flowtube[i-1][2]-flowtube[i][2]
            b = np.sqrt(dxb**2+dyb**2)
            dxc = flowtube[i][1]-flowtube[i][4]
            dyc = flowtube[i][2]-flowtube[i][5]
            c = np.sqrt(dxc**2+dyc**2)
            dxd = flowtube[i][4]-flowtube[i-1][4]
            dyd = flowtube[i][5]-flowtube[i-1][5]
            d = np.sqrt(dxd**2+dyd**2)
            dxp = flowtube[i-1][1]-flowtube[i][4]
            dyp = flowtube[i-1][2]-flowtube[i][5]
            p = np.sqrt(dxp**2+dyp**2)
            dxq = flowtube[i-1][4]-flowtube[i][1]
            dyq = flowtube[i-1][5]-flowtube[i][2]
            q = np.sqrt(dxq**2+dyq**2)
            
            quad_A1 = 0.25*np.sqrt(4*p*p*q*q-(b*b+d*d-a*a-c*c)*(b*b+d*d-a*a-c*c))
            
            dxa = flowtube[i-1][6]-flowtube[i-1][1]
            dya = flowtube[i-1][7]-flowtube[i-1][2]
            a = np.sqrt(dxa**2+dya**2)
            dxb = flowtube[i-1][1]-flowtube[i][1]
            dyb = flowtube[i-1][2]-flowtube[i][2]
            b = np.sqrt(dxb**2+dyb**2)
            dxc = flowtube[i][1]-flowtube[i][6]
            dyc = flowtube[i][2]-flowtube[i][7]
            c = np.sqrt(dxc**2+dyc**2)
            dxd = flowtube[i][6]-flowtube[i-1][6]
            dyd = flowtube[i][7]-flowtube[i-1][7]
            d = np.sqrt(dxd**2+dyd**2)
            dxp = flowtube[i-1][1]-flowtube[i][6]
            dyp = flowtube[i-1][2]-flowtube[i][7]
            p = np.sqrt(dxp**2+dyp**2)
            dxq = flowtube[i-1][6]-flowtube[i][1]
            dyq = flowtube[i-1][7]-flowtube[i][2]
            q = np.sqrt(dxq**2+dyq**2)
            
            quad_A2 =0.25*np.sqrt(4*p*p*q*q-(b*b+d*d-a*a-c*c)*(b*b+d*d-a*a-c*c))
            
            flowtube[i][9] = quad_A1+quad_A2
           
        
#print(flowtube)
np.savetxt("fta_flowtube_details.csv", flowtube, delimiter=",",header='distance,center_x,center_y,center_z,bdry1_x,bdry1_y,brdy2_x,brdy2_y,width,area_quad,area_other')








###Plot the figure
fig = plt.figure()
ax=fig.add_subplot(1,1,1)
ax.matshow(raster)
ax.streamplot(xv,yv,gradx,grady,start_points=center_point,linewidth=0.4,density=10)
ax.streamplot(xv,yv,gradx,grady,start_points=bdry1_start,linewidth=0.4,density=10)
ax.streamplot(xv,yv,gradx,grady,start_points=bdry2_start,linewidth=0.4,density=10)

#print(pits[:,0])
ax.scatter(pits[:,0],pits[:,1])
#ax.set_xlim(60,130)
#ax.set_ylim(0,90)





#plt.savefig('test.png')
#plt.matshow(raster)

plt.savefig('pomd_test.png')
plt.close()



print('done')