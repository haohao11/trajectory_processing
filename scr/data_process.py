# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 12:41:19 2018
This is the module to process the trajectory data
For each trajectory claculate:
    Heading Angle--theta, vector of the coordinates from time t to time t+1
    Orientation Adaption--alpha, the heading angle between final destination to real heading angle at each time-step
    Speed--speed, speed at each time-step
    Speed Adaption--speedAdap, the change of speed from time t to time t+1
    Absolute Speed--absoSpeed, the absolute speed to final destination
@author: cheng
"""

import os
import pickle
import numpy as np

import csv_transpose as ct

def main():
    #ct.transpose("trajectory.csv")
    frame_data, frameList, numUsers_data = sequence_precess(maxNumusers = 40)
    user_data, userID, numFrame_data = user_process(maxSeq=110)
    
    print("------------------------------------------------------------------")
    print("processed frames")    
    print("\nframe data: \n", frame_data)
    print("\nframeList: \n", frameList)
    print("\nnumUsers_data: \n", numUsers_data)
    
    print("------------------------------------------------------------------")
    print("processed users") 
    print("\nuser data: \n", user_data)
    print("\nuser ID: \n", userID)
    print("\nnumFrame_data: \n", numFrame_data)
    print("\nthe longest sequence: \n", max(numFrame_data))
    
    
def sequence_precess(maxNumusers):
    '''
    This is the function to process the trajectory data according to each frame
    params:
        maxNumusers: it is the maximum number of users in each frame
    '''
    # Numpy array corresponding to the dataset with a size (numFrame, maxNumUsers, 4)
    frame_data = []
    
    # numUsers_data is a list containing the number of users in each frame in the dataset
    numUsers_data = []
    
    
    data_dir = "..\data"
    file_path = os.path.join(data_dir, "transpose.csv")
    # Load data from the csv file
    # frameId, userId, x, y, userType
    data = np.genfromtxt(file_path, delimiter=',')
    
    # Frame IDs form the dataset, convert it to a list
    frameList = np.unique(data[0, :]).tolist()
    
    # Number of the frames in this dataset
    numFrame = len(frameList)    
    
    frame_data = np.zeros((numFrame, maxNumusers, 4))
    
    curr_frame = 0
    for index, frame in enumerate(frameList):
        # Extract all users in current frame, containing frameId, userId, x, y where frameId==frame
        usersInFrame = data[:, data[0, :] ==frame]
# =============================================================================
#         print("usersInFrame: \n", usersInFrame)
#         print("print type of usersInFrame: \n", type(usersInFrame))
# =============================================================================
        
        # Extract user list in the current frame, convert this numpy arrow to list
        usersList = usersInFrame[1, :].tolist()
        
        # Add number of users in the current frame to the current dataset to the stored data
        numUsers_data.append(len(usersList))
        
        
        # Define usersWithPos with size (userId, current_x, current_y, userType)
        usersWithPos = []
        
        # for each user in the current frame
        for userId in usersList:
            # Find the corresponding row and extract the corresponding element
            # Etract their x, y positions and userType
            current_x = usersInFrame[2, usersInFrame[1, :]==userId][0]
            current_y = usersInFrame[3, usersInFrame[1, :]==userId][0]
            userType = usersInFrame[4, usersInFrame[1, :]==userId][0]
            
            # Add the userId, x, y, userType to the row of the numpy array
            usersWithPos.append([userId, current_x, current_y, userType])
            
        # Add the details of the user in the current frame.
        # Here convert to numpy array
        frame_data[index, 0:len(usersList), :] = np.array(usersWithPos)
        
        # increment the frame index
        curr_frame += 1
        
    # Save the tuple (frame_data, frameList, numUsers_data)
    precessed_data_dir = "..\processed_data"
    if not os.path.exists(precessed_data_dir):
        print("make the folder for the processed data")
        os.mkdir(precessed_data_dir)
    data_file = os.path.join(precessed_data_dir, "ProcessedFrame.cpkl")
    f = open(data_file, "wb")
    pickle.dump((frame_data, frameList, numUsers_data), f, protocol=2)
    f.close()
    
    # Call load_sequence function
    return load_sequence(data_file)
    
    
def load_sequence(data_file):
    '''
    Function to load the pre-processed frame sequence
    '''
    
    # Load data from pickle file
    f = open(data_file, "rb")
    processed_data = pickle.load(f)
    f.close()
    
    # Get all the preprocessed data from the file
    frame_data = processed_data[0]
    frameList = processed_data[1]
    numUsers_data = processed_data[2]
    
    return frame_data, frameList, numUsers_data
    

def user_process(maxSeq):
    '''
    This is the function to process the trajectory data according to each user
    params:
        maxSeq: it is the longest sequence for the trajectory sequences
    '''
    # Read the data from csv file
    data_dir = "..\data"
    file_path = os.path.join(data_dir, "transpose.csv")
    # Load data from the csv file
    # frameId, userId, x, y, userType
    data = np.genfromtxt(file_path, delimiter=',')
    # Extract all the unique user IDs
    userID = np.unique(data[1,:]).tolist()
    numUsers = len(userID)
    
    # Initialize the user_data with size (numUsers, maxSeq, 4)
    user_data = np.zeros((numUsers, maxSeq, 4))
    
    # numFrame_data is a list containing all the frame sequences for each user
    numFrame_data = []
    
    curr_user = 0
    # Extract all the positions (x, y coordinates) for each single user
    for index, user in enumerate(userID):
        singleUserSeq = data[:, data[1, :] == user]
        frameSeq = singleUserSeq[0, :].tolist()
# =============================================================================
#         frameSeq = [int(frame) for frame in frameSeq]
#         frameSeq = frameSeq.sort()
# =============================================================================
        numFrame_data.append(len(frameSeq))
        
        # Define frameWithPos with the size (frameId, current_x, current_y, userType)
        frameWithPos = []
        for frameId in frameSeq:
            current_x = singleUserSeq[2, singleUserSeq[0, :] == frameId][0]
            current_y = singleUserSeq[3, singleUserSeq[0, :] == frameId][0]
            userType = singleUserSeq[4, singleUserSeq[0, :] == frameId][0]
            frameWithPos.append([frameId, current_x, current_y, userType])
            
        # Add the details of the sequence for the current user
        # Here convert to numpy array
        user_data[index, 0:len(frameSeq), :] = np.array(frameWithPos)
        
        # Increment the user index
        curr_user += 1
    
    # Save the tuple (user_data, userID, numFrame_data)
    precessed_data_dir = "..\processed_data"
    if not os.path.exists(precessed_data_dir):
        print("make the folder for the processed data")
        os.mkdir(precessed_data_dir)
    data_file = os.path.join(precessed_data_dir, "ProcessedUser.cpkl")
    f = open(data_file, "wb")
    pickle.dump((user_data, userID, numFrame_data), f, protocol=2)
    f.close()
    
    # Call load_user function
    return load_user(data_file)
    

def load_user(data_file):
    '''
    Function to load the pre-processed user sequence
    '''
    
    # Load data from pickle file
    f = open(data_file, "rb")
    processed_data = pickle.load(f)
    f.close()
    
    # Get all the preprocessed data from the file
    user_data = processed_data[0]
    userID = processed_data[1]
    numFrame_data = processed_data[2]
    
    return user_data, userID, numFrame_data 


            
if __name__ == '__main__':
    main()            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        

