# Mini Project

This module uses the camera on a RPI to detect aruco markers. If it detects a marker (or multiple) it will find the quadrant the marker (with the lowest id if there are mutliple detected) currently resides in. Once this information is attained it communicate this information to an arduino via a custom protocol built on the I2C stack. The arduino will then use it's highly sophisticated control systems to change the angular position of a wheel. 

Quadrants 1-4 are mapped to angular positions 0, pi/2, pi, 3pi/2 respectively.

## Run it
- Make sure a camera is connected to the Pi,
- Connect arduino via i2c to pi. 

Run ```main.py``` with python3 

```
python3 main.py
```
Use ```CTRL+C``` to exit

