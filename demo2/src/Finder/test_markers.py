from cv2 import aruco
import cv2
import numpy as np
import math
from math import cos, sin

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

camera_matrix = np.load('mat800x600.npy')
dist_coeffs = np.load('dist800x600.npy')

# Constants for linear regression
m = 0.0892
b = 0.4012

# Image is captured to bit stream and decoded
initial = cv2.imread("../../../test_pics/300cm.jpg")
img = cv2.resize(initial, (800, 600))

# Image is converted to grayscale first
# gray = cv2.cvtColor(half, cv2.COLOR_BGR2GRAY)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Thresholding is used to convert to a binary image
# Otsu's method maximizes contrast based on the input image
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# Alternative: Histogram equalization can be used
# thresh = cv2.equalizeHist(gray)

# Use built-in detection method
detection = aruco.detectMarkers(thresh, aruco_dict)
rvecs, tvecs, wvecs = aruco.estimatePoseSingleMarkers(detection[0], 76.2, camera_matrix, dist_coeffs)

# Run if markers are detected
if detection[1] is not None:
    for i in range(len(detection[1])):
        marker_id = detection[1][i][0]
        
        # Correct position
        pos = np.matrix.transpose(np.matrix(m*tvecs[i][0] + b))
        
        # Get rotation matrix of marker
        rotation_matrix = cv2.Rodrigues(rvecs[i])[0]
        
        # Scaled for 2.5 in.
        normal = np.matrix([[0], [0], [63.5]])        
        result = pos - rotation_matrix * normal
        
        x = result.item(0)
        y = result.item(1)
        z = result.item(2)
        
        angle_h = math.atan(x/z)
        angle_v = math.atan(y/z)
        
        print("Marker Stats:")
        print(x)
        print(y)
        print(z)
        print(angle_h)
        print(angle_v)
        
        # Updates marker entries in dictionary
        #markers[marker_id] = (distance, angle_h, angle_v, time.time())