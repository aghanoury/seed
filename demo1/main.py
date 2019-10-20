import numpy as np
from src import Comms
# from src import Finder

""" Main Runner Script for Demo 1 """


com = Comms("CREAMSOUP\nSUPERBOT AI")
# com.startup_color_sequence()

# Send some data
payload = [com.CHANGE_ANGLE, np.pi/2]

commands = {1: com.CHANGE_ANGLE, 2: com.CHANGE_POS}

while True:
    print("Commands\n1: Change angle\n2: Change position")
    try:
        command = commands[int(input("Enter a command: "))] 
    except KeyboardInterrupt:
        print("Keyboard Interrupt --> Exiting")
        exit(0)
    except:
        print("Invalid Option. Try again.")
        continue

    if command == com.CHANGE_ANGLE:
        angle = float(input("Targeted Angle: "))
    print("Trash")

