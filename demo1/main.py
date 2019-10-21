import numpy as np
from src import Comms
from src import Finder
import time

""" Main Runner Script for Demo 1 """
# cv parameters
f = Finder()


# robot parameters
r = 0.15/2
d = 0.275

com = Comms("CREAMSOUP\nSUPERBOT AI")
# com.startup_color_sequence()

# Send some data
# com.sendData(payload)

# exit(0)

f.start()
while True:
    result = f.markers
    print(f.markers)
    time.sleep(0.5)

exit(0)


commands = {1: com.CHANGE_ANGLE, 2: com.CHANGE_POS}

while True:
    payload = []
    print("----\nCommands\n1: Change angle\n2: Change position")
    try:
        command = commands[int(input("Enter a command: "))] 
    except KeyboardInterrupt:
        print("Keyboard Interrupt --> Exiting")
        exit(0)
    except:
        print("Invalid Option. Try again.")
        continue

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
