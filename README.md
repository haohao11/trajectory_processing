# Trajectory Processing
**This is the program that extracts trajectories from raw videos**

## Camera Calibration
**This is the first step to read the parameters for *Camera Matrix* and *Distortion Coefficiency*, etc.** 
* Shoot a short video for a dashboard at **different positions** using a **Static camera**, and save it in the folder *video*
* Unfold the dashboard vedio using **unfoldVideo.py**, name the folder for saving the unfolded images accordingly
* Compute *Camera Matrix* and *Distortion Coefficiency* using **CamCalibration.py**

## Remove Distortions in Images
**This is the second step to remove the Distortion of the recorded videos**
* Unfold the trajectory vedios using **unfoldVideo.py**, name the folder for saving the unfolded photos accordingly
* Remove the distortion using **ImgUndistortion.py**

## Extracting Trajectories
**This is the third step to extract the trajectories from the undistorted videos (images)**
* Concatenate the undistorted images into video for **_Tracker_** http://physlets.org/tracker/ (manually tracking)
  * `<ffmpeg -r 25 -i img%03d.png -c:v libx264 -vf fps=25 -pix_fmt yuv420p out.mp4>`
* or Use SiameseFC tracker http://www.robots.ox.ac.uk/~luca/siamese-fc.html

## Transform pixel coordinate system to real-world coordinate system
**This is the 4th step to convert pixel trajectories to real-world trajectories**
* Get four referencial points in both pixel coordinate and real-world coordinate systems respectively for affine transformation
* Run **CoordinateTransfer.py**

## Trajectory Visualiztion
**This is the last step to plot the trajectories**
* Run **plot_trajectory.py** to visualize the extracted trajectories

![Camera calibration](https://github.com/SocialCars/Hao_TrajectoryProcessing/blob/master/huanong_calibration/00023.jpg)
