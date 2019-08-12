

import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal

fname = "R:/feather_river_mixing_paper/dem/pomd_out.tif"

dem = gdal.Open(fname)
print('loaded dem')
#print(dem.GetMetadata)
raster = np.array(dem.GetRasterBand(1).ReadAsArray())
temp = np.flip(raster,0)
raster= temp
print(raster)
gradx = np.gradient(raster, axis = 1)
grady = np.gradient(raster, axis = 0)
print(np.shape(gradx))
print(np.shape(grady))
nx,ny=(144,150)
x = np.linspace(0, 1, nx)
y = np.linspace(0, 1, ny)
xv, yv = np.meshgrid(x, y)


seedpoint = np.array([[0.5],[0.5]])
fig = plt.figure()
plt.streamplot(xv,yv,gradx,grady,start_points=seedpoint.T)
plt.streamplot(xv,yv,gradx,grady)
plt.savefig('test.png')
plt.close()



print('done')