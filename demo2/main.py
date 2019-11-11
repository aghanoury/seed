import numpy as np
from src import Comms
from src import Finder
import time

""" Main Runner Script for Demo 1 """

# change to true to run cv
if True:
    f = Finder() # init CV object
    f.start() # starts its own thread


# robot parameters
r = 78
d = 69

# init comms obj
com = Comms()
# try:
#     com = Comms("CREAMSOUP\nSUPERBOT AI")
# except:
#     print("Failed to init Comms class")
#     print("Is the arduino on and i2c connected?\nExiting")
#     exit(14)
# com.startup_color_sequence()

PRINT_CV = 69
FIND_N_GO = 70

# small dictionary of commands
# add more commands to the comms class
cmds = com.commands

# added tmp commands
cmds['debug CV'] = PRINT_CV
cmds['FIND_N_GO'] = FIND_N_GO

# commands = {"angle change": com.CHANGE_ANGLE, "linear traverse": com.}
# commands = {1: com.ROTATE, 2: com.LINEAR_TRAVERSE, 3: PRINT_CV, 4: FIND_N_GO}


# continously prompt for user commands
while True:

    # print menu options
    for i in range(len(cmds)):
        print("{}: {}".format(i+1,list(cmds)[i]))


    # get user input
    try:
        key = list(cmds)[int(input("Command: "))-1]
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





    elif command == PRINT_CV:

        while True:
            try:
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
                print(result)
                time.sleep(0.1)

            except KeyboardInterrupt:
                break

    elif command == FIND_N_GO:

        while True:
            if(input("Auto Detect [y/n]: ") == 'y'):
                timeout = time.time() + 15   # 5 minutes from now
                com.search()

                try:
                    while f.did_detect == False:
                        if time.time() > timeout:
                            print('Timeout')
                            break
                except KeyboardInterrupt:
                    print("Keyboard interrupt. Returning to Home")
                    com.stop()
                    break
                com.stop()

                time.sleep(2)
                result = f.markers
                distance = round(result[0][0]/100,3)
                angle = round(-result[0][1],3)
                
                try:
                    print(distance, angle)
                    com.rotate(angle, radians=True)
                    time.sleep(2)
                    print(distance)
                    com.linTraverse(distance-0.9,meters=True)
                    time.sleep(9)
                    print(type(result),result)
                    distance = round(result[0][0]/100/3.281,3)
                    print(distance)
                    com.rotate(-90)
                    time.sleep(4)
                    com.stop()
                    time.sleep(1)
                    com.circularTraverse(1.4*0.3048, direction='left')
                    time.sleep(7)
                except KeyboardInterrupt:
                    print("Keyboard interrupt. Returning to Home")
                    com.stop()
                    break



                # print("Distance: {}    Angle: {} ".format(distance, angle))
                # print(f.did_detect)
                # time.sleep()
            



            else:
                break