import numpy as np
from src import Comms
from src import Finder
import time
import RPi.GPIO as gpio



""" Main Runner Script for Demo 2 """

f = Finder() # init CV object
# f.start() # starts its own thread



# init comms obj
try:
    # you can init comms with robot parameters
    # we are using defualt values
    com = Comms() 
except:
    print("FAILED TO INIT COMMS\nIs arduino on?")



# configure GPIO to read robots status
# eventually should move into comms class but had a weird
# issue with calling GPIO functions from a parent scope
gpio.setmode(gpio.BCM)
gpio.setup(17, gpio.IN)

# custom routines, values are arbitrary
PRINT_CV = 69
FIND_N_GO = 70
REQUEST = 80
# get prebuilt commands
cmds = com.commands
# added tmp commands
cmds['debug CV'] = PRINT_CV
cmds['FIND_N_GO'] = FIND_N_GO
cmds['request data'] = REQUEST



# continously prompt for user commands
while True:

    # print menu options
    for i in range(len(cmds)):
        print("{}: {}".format(i+1,list(cmds)[i]))


    # get user input
    try:
        inp = input("Commands: ")
        if inp == 'e':
            print("EXITING")
            exit(0)
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

            direction = input("l or r? (press enter for defautl): ")
            
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

        # get some flags
        direction = input('Search left or right [l/r]: ')
        rotate = input('Rotate at end [y/n]: ')


        while True:
            try:
                timeout = time.time() + 25
                f.find_markers()
                # com.search() 
                # begin serach
                while f.did_detect == False:
                    if direction == 'r':
                        com.rotate(-25)
                    else:
                        com.rotate(25)
                
                    wait(0.1)
                    f.find_markers()
                    if time.time() > timeout:
                        print('Timeout')
                        break
                        
                com.stop()
                time.sleep(2)
                if not f.did_detect:
                    print("Did not find a marker")
                    break
                
                distance = round(f.markers[0][0]/100,3)
                angle = round(-f.markers[0][1],3)
                
                print("Found Marker {} meters {} radians".format(distance, angle))
                com.rotate(angle, radians=True)
                wait(0.2)

                com.linTraverse((distance)-0.35,meters=True)
                wait(0.2)

                distance = round(result[0][0]/100,3)
                print("Distance: ", distance)

                if rotate == 'y':
                    com.rotate(-90)
                    wait(0.2)

                    com.circularTraverse(1.4*0.3048, direction='left')
                    wait(0.2)
                
            except KeyboardInterrupt:
                print("Keyboard interrupt. Returning to Home")
                com.stop()
                break


def wait(delay=0.3, timeout=15):
    timout = time.time() + timeout
    time.sleep(delay)
    while gpio.input(17) == False:
        if time.time() > timeout:
            print("FAILED TO VERIFY MOTION TERMINATION\nEXITING")
            exit(-1) 