from picamera import PiCamera
import os
import time

class Capturer:
    def __init__(self):
        # Init function sets up camera
        self.camera = PiCamera()
        # Make resolution smaller to increase speed, larger to increase accuracy
        # Note: different resolutions require different camera calibration
        self.camera.resolution = (800, 600)
        #self.camera.resolution = (1920, 1080)
        self.camera.exposure_mode = 'off'
        self.camera.shutter_speed = 10000
        self.camera.awb_mode = 'off'
        self.camera.iso = 1600
        
        self.marker_detection = {}
        self.folder = 'Captures'

        try:
            os.mkdir(self.folder)
        except FileExistsError:
            pass
                
    def capture_loop(self):
        val = ''
        while True:
            val = input("Capture Image? q to quit")
            if val == 'q':
                break
            capture()
            
    
    def capture(self):
        self.camera.capture(os.path.join(self.folder, '{}.png'.format(time.time())), format='jpeg', use_video_port=True)

c = Capturer()
c.capture_loop()