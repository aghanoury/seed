import numpy as np
from src import Comms
from src import Finder
import time

""" Main Runner Script for Demo 1 """

# init CV object
f = Finder()


# robot parameters
r = 0.15/2
d = 0.270

# init comms obj
try:
    com = Comms("CREAMSOUP\nSUPERBOT AI")
except:
    print("Failed to init Comms class")
    print("Is the arduino on and i2c connected?\nExiting")
    exit(14)
# com.startup_color_sequence()

# start CV processing thread
f.start() # starts its own thread

PRINT_CV = 4

# small dictionary of commands
commands = {1: com.CHANGE_ANGLE, 2: com.CHANGE_POS, 3: PRINT_CV}


# continously prompt for user commands
while True:
    payload = []
    print("----\nCommands\n1: Change angle\n2: Change position\n3: Detect Marker")
    try:
        # get user input
        command = commands[int(input("Enter a command: "))] 
    except KeyboardInterrupt:
        print("Keyboard Interrupt --> Exiting")
        exit(0)
    except:
        print("Invalid Option. Try again.")
        continue

    # process user input
    if command == com.CHANGE_ANGLE:
        payload = [com.CHANGE_ANGLE]

        angle1 = float(input("Targeted Angle Left (Deg): "))
        # angle2 = float(input("Targeted Angle Right (Deg): "))
        angle1 *= np.pi/180 
        # angle2 *= np.pi/180 * 2

        theta = angle1 * d / r
        payload.append(theta)
        payload.append(theta)

        com.sendData(payload)

    elif command == com.CHANGE_POS:
        payload = [com.CHANGE_POS]

        dist = float(input("Targeted Distance (ft): "))
        dist = dist/3.281
        theta = dist / r * 2
        payload.append(-theta)
        payload.append(theta)

        com.sendData(payload)

    elif command == PRINT_CV:

        while True:
            result = f.markers
            com.lcd.clear()
            try:
                st = "Dist: {}\nAng: {}".format(str(round(result[0][0]/30.48,3)),str(round(-1*result[0][1]*180/np.pi,3)))
            except:
                st = "None"
            com.lcd.message = st
            print(result)
            time.sleep(1)
