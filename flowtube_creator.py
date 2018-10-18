# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 12:48:31 2018

@author: LHMK
"""
###Flowtube creator file for LSDMixingModel
###This script loads a hillslope raster and transect data and uses them to find the following parameters for use in the LSDMixingModel:
##Parameters found 
#number of nodes to model the transect
#downslope distance of those nodes (ds_dist)
#width of flowtube (width)
#Area of flowtube surface (A_poly)
#Elevation of nodes (meas elev)
import numpy as np
import richdem as rd


###Input the parameters
#Gridded data e.g.raster file
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

