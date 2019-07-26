import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline, BSpline
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/mixing_0_0001/'
DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/mixing_0_0001_erosion_0_001/'
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/no_mixing/'
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/flux_tests/no_mixing_erosion_0_001/'


#Load the relevant data
hillslope = pd.read_csv(DataDirectory+'ft_properties.out', sep=" ",header=0,comment='-')
zeta = pd.read_csv(DataDirectory+'zeta_trans.zdat', sep=" ",index_col=0,header=None)
eta = pd.read_csv(DataDirectory+'eta_trans.edat', sep=" ",index_col=0,header=None)
h =pd.read_csv(DataDirectory+'h_trans.hdat', sep=" ",index_col=0,header=None)
#print(hillslope)
#print(zeta)
#print(eta)
#print(h)
#Set the max values for plotting the spline
h_min = hillslope['s'].min()
h_max = hillslope['s'].max()

###This should be put in a loop soon to allow plotting of multiplt timesteps


fig = plt.figure()
ax = fig.add_subplot(1,1,1)
#Plot the surface
ax.scatter(hillslope['s'],zeta,s=5,c='k',marker="_")
#Plot the surface of the saprolite
ax.scatter(hillslope['s'],eta,s=5,c='k',marker="_")
#Plotting fucntions for putting a curved line through the surfaces
#Plot the line
hillslope_line = np.linspace(h_min,h_max,100)
#Here is some annoying array conversion that probs isn't needed but to do with pandas dataframes and the spline stuff
#Note that when fitting a monotonic function the x array must be varying constantly, this will most likely be the error if it doesnt work.
hl_arr =np.array(hillslope['s'])
z_arr = np.array(zeta.iloc[0])
e_arr = np.array(eta.iloc[0])
#Make the lines
z_spl=make_interp_spline(hl_arr,z_arr,k=3)
e_spl=make_interp_spline(hl_arr,e_arr,k=3)
zeta_smooth = z_spl(hillslope_line)
eta_smooth = e_spl(hillslope_line)
#Plot the lines
plt.plot(hillslope_line,zeta_smooth,linewidth=1,c='k')
plt.plot(hillslope_line,eta_smooth,linewidth=1,c='k')
#Fill the lines with a fetching brown colour to help see it, change later
ax.fill_between(hillslope_line, zeta_smooth, eta_smooth, color='saddlebrown')
#Save the figure
plt.savefig(DataDirectory+'catena_profile', dpi=100, bbox_inches='tight')

