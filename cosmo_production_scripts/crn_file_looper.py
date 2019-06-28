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
#set figure size
fig = plt.figure(figsize=(10,10))
ax=fig.add_subplot(1,1,1)

for subdirs, dirs, files in os.walk(root):
    for dirs in dirs:
        data = pd.read_csv(root+dirs+'/p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
        print('loaded '+str(dirs))
        be_conc =data['be_conc'].values
        d_loc = data['d_loc'].values
        cm = np.full(len(be_conc),counter)
        cb = ax.scatter(be_conc,d_loc,s=0.2,c=cm,cmap=plt.cm.viridis,lw = 0, alpha=0.25)
        cb.set_clim(vmin=1,vmax=runs)
        #temp_name = str(root)+str(dirs)
        #print(temp_name)
        counter+= 1

ax.set_ylim(0,3)        
plt.gca().invert_yaxis()    
axcb = plt.colorbar(cb)
plt.show()
plt.savefig(root+'be_conc_depth_changing_mixing', dpi=100, bbox_inches='tight')
