# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 12:48:31 2018

@author: LHMK
"""
###Flowtube creator file for LSDMixingModel, reqiore RICHDEM and Rasterio packages installed 
###This script loads a hillslope raster and transect data and uses them to find the following parameters for use in the LSDMixingModel:
##Parameters found 
#number of nodes to model the transect
#downslope distance of those nodes (ds_dist)
#width of flowtube (width)
#Area of flowtube surface (A_poly)
#Elevation of nodes (meas elev)

import matplotlib
matplotlib.use("Agg")
import numpy as np
import richdem as rd
from matplotlib import pyplot as plt

###Input the parameters
#Gridded data e.g.raster file
#Load the data and convert it to an array for RichDEM
fname = 'L:/feather_river_mixing_paper/dem/pomd_out.tif'
# Loading the raster with rasterio


raster = rd.LoadGDAL(fname)

#rasterfig = rd.rdShow(raster, ignore_colours=[0], axes=False, cmap='gist_earth', figsize=(8,5.5))

raster_filled = rd.FillDepressions(raster, epsilon=True, in_place=False)

#rasterfig_filled = rd.rdShow(raster_filled, ignore_colours=[0], axes=False, cmap='gist_earth', vmin=rasterfig['vmin'], vmax=rasterfig['vmax'], figsize=(8,5.5))

accum_d8 = rd.FlowAccumulation(raster_filled, method='D8')
#d8_fig = rd.rdShow(accum_d8, figsize=(8,5.5), axes=False, cmap='jet')

slope=rd.TerrainAttribute(raster_filled, attrib='slope_riserun')
#rd.rdShow(slope, axes=False, cmap='jet', figsize=(8,5.5))

profile_curvature = rd.TerrainAttribute(raster_filled, attrib='curvature')
#rd.rdShow(profile_curvature, axes=False, cmap='jet', figsize=(8,5.5))


print (raster)
temp = np.flip(raster,0)
raster= temp
print(raster)
x=np.size(raster,1)
y=np.size(raster,0)
print (x)
print (y)
gradient = np.empty((8,x-2,y-2),dtype=np.float)
for k in range(8):
    theta = -k*np.pi/4
    j, i = np.int(1.5*np.cos(theta)),-np.int(1.5*np.sin(theta))
    d = np.linalg.norm([i,j])
    gradient[k] = (raster[1+i: y-1+i,1+j: x-1+j]-raster[1: y-1,1: x-1])/d
direction = (-gradient).argmax(axis=0)
print (direction)

####Work out what ius going on here



#Check differences between raster
#raster_diff = raster_filled-raster
#rasterfig_diff = rd.rdShow(raster_diff, ignore_colours=[0], axes=False, cmap='jet', figsize=(8,5.5))
#s
#Depth data with x,y,z locations of pits along with soil depth, this must be in the same format as the gridded data and from this intermediuate pits can be calculated


###Running the script
#Find the streamline down between the pits to get the center of the flowtube

#Then find the 2 boundaries of it by giving an initial max width by following along the contours until you reach the predetermined max 
 
#Now run the streamline for both these boundary lines
 
#Go down each flowpath collecting the elevation and downstream distance data
 
#Now go through each pit/intermediate pit point and find the corresponding point of the boundary flow lines on the contour
 
#For each node we then follow th econtour through the points to get the widths
 
#Then we find the area either by finding the area of a quadrilateral or by some fancy curvilinear thing I still need to check
 
#Now output all the relvant data to a ft_details.param file

