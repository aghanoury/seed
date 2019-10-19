import numpy as np
from src import Comms
# from src import Finder

""" Main Runner Script for Demo 1 """


com = Comms("CREAMSOUP\nSUPERBOT AI")
# com.startup_color_sequence()

# Send some data
print(np.pi/2)
com.sendData([com.WRITE_ANGLE, np.pi/2])
