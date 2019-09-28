from src import Finder
from src import Comms 
import time


comm = Comms()
print("Successfull init of Comms class")

f = Finder()
print("Successfull init of Finder class")

# f.find_markers(0.5)


while True:
    target_position = input("Enter quadrant of ChArUco: ")
    if target_position == 'exit':
        print("exiting")
        exit(0)
    # comm.
