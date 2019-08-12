import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
import os as os

#Set the root directory
root = 'C:/Workspace/github/LSDMixingModel/Runs/bull_lake/'
#set number of runs
runs = (len(next(os.walk(root))[1]))
print(runs)
counter = 1
#Create bins, to do this need to set depth first
d =1.5
bins = np.linspace(0,d,15)
#set figure size
fig = plt.figure(figsize=(10,10))
ax=fig.add_subplot(1,1,1)

#Now loop through the p_trans_out files and plot them on the same graph

data = pd.read_csv(root+'runmixing_0_0001/'+'p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
#Cut off all depth data below the depth set earlier
data = data.drop(data[data.d_loc >= d].index)
ax.scatter(data['be_conc'],data['d_loc'],c='k',s=1)
        
        
        
        
        
        
        
#Now load the initial data to test the model against
initial_data = pd.read_csv('C:/Workspace/github/ModelTesting/master_param/bull_lake/bull_lake.csv', sep=",",skiprows=[0], names =['upp_d','low_d','be_conc','depth','d_err','be_err'])
#print(initial_data)
be_conc = initial_data['be_conc'].values
#Convert the values to be the same as the outputted data
be_conc = be_conc*100000
#print(be_conc)
d_loc = initial_data['depth'].values
#print(d_loc)
ax.scatter(be_conc,d_loc,s=20,c='r')
ax.set_ylim(0,d)        
plt.gca().invert_yaxis()    
plt.show()
#plt.savefig(root+'be_conc_depth_changing_mixing', dpi=100, bbox_inches='tight')