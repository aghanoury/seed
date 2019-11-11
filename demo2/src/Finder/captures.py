from picamera import PiCamera
import os

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
        self.marker_detection = {}

        try:
            os.mkdir('Captures')
        except FileExistsError:
            pass
            
        self.count = 0;
    
    def capture_loop():
        val = ''
        while True:
            val = input("Capture Image? q to quit")
            if val == 'q':
                break
            camera.capture(os.path.join(folder, '{}.png'.format(self.count)))
            self.count += 1

c = Capturer()
c.capture_loop()