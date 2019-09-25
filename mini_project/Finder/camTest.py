import numpy.core.multiarray
from picamera import PiCamera
from time import sleep
from cv2 import aruco
import cv2
import io
import numpy as np
import time

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

camera = PiCamera()
#camera.resolution = (800, 600)
#camera.resolution = (2592, 1944)
camera.resolution = (1920, 1080)
camera.exposure_mode = 'off'
camera.shutter_speed = 10000
camera.awb_mode = 'off'

checkpoint = time.time()
img_stream = io.BytesIO()
camera.capture(img_stream, 'jpeg')
img_stream.seek(0)
img_bytes = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
print("Capture Time:", time.time() - checkpoint)

checkpoint = time.time()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print("Grayscale Time:", time.time() - checkpoint)

checkpoint = time.time()
hist = cv2.equalizeHist(gray)
print("Histogram Time:", time.time() - checkpoint)

checkpoint = time.time()
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
print("Threshold Time:", time.time() - checkpoint)

cv2.imwrite('capture.jpg', img)
cv2.imwrite('gray.jpg', gray)
cv2.imwrite('hist.jpg', hist)
cv2.imwrite('thresh.jpg', thresh)

checkpoint = time.time()
x = aruco.detectMarkers(hist, aruco_dict)
print("Detection Time:", time.time() - checkpoint)

print("Detected Markers:")
print(x[1])

checkpoint = time.time()
x = aruco.detectMarkers(thresh, aruco_dict)
print("Detection Time:", time.time() - checkpoint)

print("Detected Markers:")
print(x[1])

result = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
result = aruco.drawDetectedMarkers(result, x[0])
cv2.imwrite('marks.jpg', result)
