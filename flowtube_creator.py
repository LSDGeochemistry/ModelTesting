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
import numpy as np
import richdem as rd
import rasterio as rio

###Input the parameters
#Gridded data e.g.raster file
#Load the data and convert it to an array for RichDEM
fname = 'L:/feather_river_mixing_paper/dem/pomd_out.tif'
# Loading the raster with rasterio
this_raster = rio.open(fname)

# Initialising a dictionary containing the raster info for output
out = {}
gt = this_raster.res
out['res'] = gt[0]
out["ncols"] = this_raster.width+1
out["nrows"] = this_raster.height+1
out["x_min"] = this_raster.bounds[0]-out['res']
out["y_min"] = this_raster.bounds[1]-out['res']
out["x_max"] = this_raster.bounds[2]+out['res']
out["y_max"] = this_raster.bounds[3]+out['res']
out["extent"] = [out["x_min"],out["x_max"],out["y_min"],out["y_max"]]
out["array"] = this_raster.read(1)# rd.rdarray(np.pad(this_raster.read(1).astype(np.float32), 1, 'constant',constant_values = -9999), no_data = -9999.)
out['nodata'] = this_raster.nodatavals
# This bit is to adapt the array to richdem
pomd = rd.rdarray(out, no_data=out['nodata'])
out["array"].geotransform = (this_raster.transform[2],this_raster.transform[0],this_raster.transform[1],this_raster.transform[5],this_raster.transform[3],this_raster.transform[4])
out['crs'] = this_raster.crs['init']



print ('done')

pomd = rd.rdarray(out, no_data=out['nodata'])

pomdfig = rd.rdShow(pomd, ignore_colours=[0], axes=False, cmap='jet', figsize=(8,5.5))
#pomd_filled = rd.FillDepressions(pomd, in_place=False)
#pomdfig_filled = rd.rdShow(pomd_filled, ignore_colours=[0], axes=False, cmap='jet', vmin=pomdfig['vmin'], vmax=pomdfig['vmax'], figsize=(8,5.5))

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

