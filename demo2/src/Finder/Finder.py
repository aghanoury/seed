import numpy.core.multiarray
from picamera import PiCamera
from time import sleep
from cv2 import aruco
import cv2
import io
import numpy as np
import threading
import math
import time

# Aruco dictionary used
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

# Constants for linear regression
m = 0.0892
b = 0.4012

# Markers are 3 in, or 76.2 mm
marker_width = 76.2

class Finder:
    def __init__(self):
        # Init function sets up camera
        self.camera = PiCamera()
        # Make resolution smaller to increase speed, larger to increase accuracy
        # Note: different resolutions require different camera calibration
        self.camera.resolution = (800, 600)
        #self.camera.resolution = (1920, 1080)
        self.camera.exposure_mode = 'off'
        self.camera.shutter_speed = 7000
        self.camera.awb_mode = 'off'
        self.marker_detection = {}
        
        # Camera calibration for 800x600 images
        # self.camera_matrix = np.load('mat800x600.npy')
        # self.dist_coeffs = np.load('dist800x600.npy')

        # absolute paths
        self.camera_matrix = np.load('src/Finder/mat800x600.npy')
        self.dist_coeffs = np.load('src/Finder/dist800x600.npy')
        
        self.markers = {}
        self.run_thread = True
        
        self.thread = threading.Thread(target=self.detection_thread)
        self.did_detect = False
    
    def start(self):
        # Easy method to start marker detection
        self.thread.start()
        
    def stop(self):
        # Easy method to stop marker detection
        self.run_thread = False
        self.thread.join()
        
    def detection_thread(self):
        # Thread runs until stopped
        while self.run_thread :
            self.find_markers()
            #print(self.markers)

    def find_markers(self):
        # Image is captured to bit stream and decoded
        img_stream = io.BytesIO()
        self.camera.capture(img_stream, 'jpeg')
        detect_time = time.time();
        img_stream.seek(0)
        img_bytes = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
        img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
        
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
        rvecs, tvecs, wvecs = aruco.estimatePoseSingleMarkers(detection[0], 76.2, self.camera_matrix, self.dist_coeffs)
        

        # Run if markers are detected
        if detection[1] is not None:
            new_detection = {}
            self.did_detect = True
            for i in range(len(detection[1])):
                marker_id = detection[1][i][0]
                
                # Correct position
                pos = np.matrix.transpose(np.matrix(m*tvecs[i][0] + b))
                
                # Get rotation matrix of marker
                rotation_matrix = cv2.Rodrigues(rvecs[i])[0]
                
                # Scaled for 2.5 in.
                normal = np.matrix([[0], [0], [6.35]])        
                result = pos - rotation_matrix * normal
                
                x = result.item(0)
                y = result.item(1)
                z = result.item(2)
                
                angle_h = math.atan(x/z)
                angle_v = math.atan(y/z)
                
                # Angle Correction
                angle_h = angle_h*1.1136 - 0.0109
                
                # Updates marker entries in dictionary
                if self.markers.has_key(marker_id) and self.markers[marker_id][3] == detect_time:
                    m = self.markers[marker_id]
                    z_avg = (m[0] + z)/2
                    h_avg = (m[1] + angle_h)/2
                    v_avg = (m[2] + angle_v)/2
                    self.markers[marker_id] = (z_avg, h_avg, v_avg, detect_time)
                else:
                    self.markers[marker_id] = (z, angle_h, angle_v, detect_time)
                # self.markers[marker_id] = (z, angle_h, angle_v, time.time())
        else:
            self.did_detect = False
                
