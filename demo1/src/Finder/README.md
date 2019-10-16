The Finder package will determine the distance and bearing of each detected marker

To import the Finder class, use the following line:

from Finder.Finder import Finder


An object can be created like so:

f = Finder()


The Finder will operate in a thread to detect markers, this process can be started like so:

f.start()


To get the position of markers, use the following line:

f.markers


This will return a dictionary like so:

{Marker ID : (Distance, Horizontal Bearing, Vertical Bearing, Time of Measurement), Marker ID...}

Currently, distance is in centimeters, angles are in radians, and time is the direct result of calling time.time()


When finishing operation, use the following command to stop the Finder thread:

f.stop()


Review the file test.py for example implementation