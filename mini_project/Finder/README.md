The Finder package will determine the quadrant of detected ArUco markers.

To import the Finder class, use the following line:
from Finder.Finder import Finder

An object can be created like so:
f = Finder()

To get the position of markers, use the following line:
f.find_markers()

This will return a list of tuples like so:
[(&lt;ID&gt;, &lt;Quadrant&gt;), (&lt;ID&gt;, &lt;Quadrant&gt;), ...]