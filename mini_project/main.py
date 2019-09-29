from src import Finder
from src import Comms 
import time
import numpy as np
import struct # might remove
from threading import Thread

try:
    comm = Comms()
    print("Successfull init of Comms class")
except:
    print("failed to load comms class")
    exit(-1)

try:
    f = Finder()
    print("Successfull init of Finder class")
except Exception as e:
    print(e)
    print("\nFailed to load finder class, program will continue")


# f.find_markers(0.5)
# comm.startup_color_sequence()

# map quadrants to angles
quad_to_ang = {1: 0.0, 2: np.pi/2, 3: np.pi, 4: 3*np.pi/2}

def updateAngle(command):
    target_position = 3
    packet = [comm.WRITE_ANGLE, quad_to_ang[target_position]]
    comm.sendData(packet)
    time.sleep(0.1)
    while True:
        val = comm.getData(command)
        
        time.sleep(0.01)
        # comm.lcd.clear()
        # comm.lcd.message = "Angular Pos\n{}".format(val)
        time.sleep(0.3)

# time.sleep(1)
# t = Thread(target=updateAngle, args=(comm.READ_ANGLE,))
# t.start()

while True:
    try:
        target_position = int(input("Enter quadrant (int -> 1-4): "))
        if target_position < 1 or target_position > 4:
            raise Exception('Invalid Quadrant')
    except Exception as e:
        print(e)
        continue
    

    packet = [comm.WRITE_ANGLE, quad_to_ang[target_position]]
    comm.sendData(packet)
    # comm.getData(comm.READ_ANGLE)