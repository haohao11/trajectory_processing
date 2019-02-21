# -*- coding: utf-8 -*-
"""
Created on Thu May  3 15:05:11 2018
This is the modular for converting from one coordinate system to another coordinate system using perspective transformation
@author: cheng
"""
import cv2
import sys
import os
import numpy as np
from numpy import genfromtxt

def main():    
    dirname = '..\data'
    data = genfromtxt(os.path.join(dirname, 'origin_coordinates.csv'), delimiter=',')
    oricoor_data = data[:, 2:4]
    
    # This reference systen is for the dataset Huanong DSCF1394
    # Get the referencial points: four points from the image coordinate system and the corresponding points from the real world coordinate system
    cols = 1920 # image width
    rows = 1080 # image height
    pts1 = np.float32([[473.5,677.3],[1037,644],[1739,661.6],[1854,817.3]]) # four points from the image coordinate system
    pts2 = np.float32([[590, 820],[1280, 1100],[1250, 1630],[420, 1720]]) # four points from the geographic coordinate system correspondingly
    # Get the transformation matrix
    M = cv2.getPerspectiveTransform(pts1, pts2)
    
    # Transform the image using the transform matrix
    # "two-channel or three-channel floating-point array, where each element is a 2D/3D vector"
    oricoor_data = np.array([oricoor_data]) # add one more dimension, which translates in Python/NumPy to a 3-dimensional array.
    dst = cv2.perspectiveTransform(oricoor_data, M, (int(cols), int(rows)))
    dst = np.squeeze(dst, axis=0)
    print(' \n real xy-coordinates:')
    #print(dst)
    #print(data[:, 0:2].shape)
    #print(data[:, 4].reshape(-1, 1))
    userType = data[:, 4].reshape(-1, 1)
    tarcoor_data = np.concatenate((data[:, 0:2], dst, userType), axis=1)
    print(tarcoor_data)
    #np.savetxt("xy-coordinates/ped1_geographic-coordinates.csv", dst, delimiter=",")
    np.savetxt(os.path.join(dirname, 'target_coordinates.csv'), tarcoor_data, delimiter=",")

if __name__ == '__main__':
    main()
    
