import numpy as np
from src import Comms
from src import Finder
import time
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(17, gpio.IN)


""" Main Runner Script for Demo 1 """

# change to true to run cv
if True:
    f = Finder() # init CV object
    # f.start() # starts its own thread


# robot parameters
r = 78
d = 69

# init comms obj
com = Comms()
time.sleep(1)
# com.start_state_detection()
# try:
#     com = Comms("CREAMSOUP\nSUPERBOT AI")
# except:
#     print("Failed to init Comms class")
#     print("Is the arduino on and i2c connected?\nExiting")
#     exit(14)
# com.startup_color_sequence()

PRINT_CV = 69
FIND_N_GO = 70
REQUEST = 80

# small dictionary of commands
# add more commands to the comms class
cmds = com.commands

# added tmp commands
cmds['debug CV'] = PRINT_CV
cmds['FIND_N_GO'] = FIND_N_GO
cmds['request data'] = REQUEST

# commands = {"angle change": com.CHANGE_ANGLE, "linear traverse": com.}
# commands = {1: com.ROTATE, 2: com.LINEAR_TRAVERSE, 3: PRINT_CV, 4: FIND_N_GO}


# continously prompt for user commands
while True:

    # print menu options
    for i in range(len(cmds)):
        print("{}: {}".format(i+1,list(cmds)[i]))


    # get user input
    try:
        inp = input("Commands: ")
        key = list(cmds)[int(inp)-1]
        command = cmds[key]
    except KeyboardInterrupt:
        print("Keyboard Interrupt --> Exiting")
        exit(0)
    except:
        print("Invalid Option. Try again.")
        continue

    """ Process User Input """
    if command == com.ROTATE:
        try: target = float(input("Target Angle (deg): "))
        except: print("Invalid Value")
        com.rotate(target)
  

    elif command == com.LINEAR_TRAVERSE:
        try: target = float(input("Target Distance (ft): "))
        except: print("Invalid Value")
        com.linTraverse(target)
            
            
    elif command == com.STOP:
        com.stop()

    elif command == com.SEARCH:
        com.search()


    elif command == com.CIRCULAR_TRAVERSE:
        try:
            target_radius = float(input("Target Radius (ft) "))
            target_radius /= 3.281

            direction = input("l or r? (default is l, ccl): ")
            
        except: print("Invalid Value")
        
        if direction == '' or 'l':
            com.circularTraverse(target_radius)
        elif direction == 'r':
            com.circularTraverse(target_radius, direction='right')
        else:
            print("invalid direction")


    elif command == REQUEST:
        print(gpio.input(17))



    elif command == PRINT_CV:

        while True:
            try:
                f.find_markers()
                result = f.markers
                distance = round(result[0][0]/100,3)
                angle = round(result[0][1],3)
                
                print(distance, angle)
                com.lcd.clear()
                try:
                    st = "Dist: {}\nAng: {}".format(str(round(result[0][0]/30.48,3)),str(round(-1*result[0][1]*180/np.pi,3)))
                except:
                    st = "None"
                com.lcd.message = st
                # print(result)
                time.sleep(0.1)

            except KeyboardInterrupt:
                break

    elif command == FIND_N_GO:

        while True:
            if(input("Auto Detect [y/n]: ") == 'y'):
                timeout = time.time() + 25   # 5 minutes from now
                f.find_markers()
                com.search()
                try:
                    while f.did_detect == False:
                        com.rotate(25)
                        time.sleep(0.5)
                        f.find_markers()
                        if time.time() > timeout:
                            print('Timeout')
                            break
                        
                except KeyboardInterrupt:
                    print("Keyboard interrupt. Returning to Home")
                    com.stop()
                    break
                
                com.stop()

                time.sleep(2)
                if not f.did_detect:
                    print("Did not find a marker")
                    break
                
                result = f.markers
                distance = round(result[0][0]/100,3)
                angle = round(-result[0][1],3)
                
                try:
                    print(distance, angle)
                    com.rotate(angle, radians=True)
                    time.sleep(0.2)
                    while gpio.input(17) == False: pass

                    com.linTraverse((distance)-0.40,meters=True)
                    time.sleep(0.2)
                    while gpio.input(17) == False: pass

                    distance = round(result[0][0]/100,3)
                    print("Distance: ", distance)
                    com.rotate(-90)
                    time.sleep(0.2)
                    while gpio.input(17) == False: pass

                    com.circularTraverse(1.4*0.3048, direction='left')
                    time.sleep(0.2)
                    while gpio.input(17) == False: pass

                except KeyboardInterrupt:
                    print("Keyboard interrupt. Returning to Home")
                    com.stop()
                    break

            else:
                break