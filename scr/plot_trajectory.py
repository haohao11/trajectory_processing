# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 11:00:40 2018
This is the module to plot related trajectories

@author: cheng
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
from matplotlib.font_manager import FontProperties

import csv_transpose as ct
import data_process as dp

def main():
    
    # Load processed data
    ct.transpose("target_coordinates.csv")
    frame_data, frameList, numUsers_data = dp.sequence_precess(maxNumusers = 80)
    user_data, userID, numFrame_data = dp.user_process(maxSeq=300)
    
    # trajectory = user_data[0, 0:22, 1:3]
    
    print(user_data)
    
    plt.figure()
    ax1 = plt.axes()
    # ax1 = plt.axes(xlim=(0, 101))
    for user, trajectory in enumerate(user_data):
        if user < 2000:
            seq_length = sum(np.count_nonzero(trajectory, axis=0)) / 4
            seq_length = int(seq_length)
            pos_x = trajectory[0:seq_length, 1]# scale up to meter ba multiple 100
            pos_y = trajectory[0:seq_length, 2]# scale up to meter ba multiple 100
            # Extract the userType
            userType = int(trajectory[0,3])
            # Define the color regarding to userType
            if userType == 1: # pedestrian
                color = '#1f77b4'
                alpha = 1.0
            elif userType == 2: # cyclist
                color = 'lawngreen'
                alpha = 0.0
            elif userType == 3: # vehicle
                color = '#ff7f0e'
                alpha = 1.0
                
            # print(seq_length)
            # print("trajectory: \n", trajectory[0:seq_length, :])
# =============================================================================
#             # use the markersize and/or opacity to illustrate the heading direction
#             for t in range(seq_length):
#                 ax1.plot(pos_x[t:t+2], pos_y[t:t+2], color=color, linestyle='dashdot', marker='D', markersize=1+t*0.2)
# =============================================================================
            ax1.plot(pos_x, pos_y, color=color, linestyle='-', linewidth=0.5, alpha=alpha)
            
    plt.plot([], [], color='#1f77b4', linestyle='-', linewidth=1.5, alpha=1, label='ped.')
    plt.plot([], [], color='lawngreen', linestyle='-', linewidth=1.5, alpha=1, label='cyc.')
    plt.plot([], [], color='#ff7f0e', linestyle='-', linewidth=1.5, alpha=1, label='veh.')    
    fontP = FontProperties()
    fontP.set_size('medium')        
                
    plt.xlabel('X-coordinate (m)')
    plt.ylabel('Y-coordinate (m)')
    #plt.title('Accumulated trajectories in a shared space')
    plt.axis('on')
    
    # plt.legend(loc='center left', bbox_to_anchor=(0.715, 0.12), prop = fontP)
    plt.legend(loc='lower right', bbox_to_anchor=(1.0, 0.0), prop = fontP)
    
    plt.show()
    
    #plt.savefig('../fig/test/' + 'hh_dataset.pdf', dpi=800)
    plt.gcf().clear()
    plt.close()
    

if __name__ == '__main__':
    main() 