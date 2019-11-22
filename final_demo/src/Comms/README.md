# Comms - Finale

The past assignments were key challenges that helped develop the foundation for communications. In demo 1, we developed the necessary lower-level protocols needed for basic command and control. It was also a great time for establishing the accruacy of our control algorithms. In demo 2, we abstracted procedures to simple commands and protocols

In Demo 2, however, we expereinced certain pitfalls with I2C. Not so much an I2C issue but rather the issue of data corruption. This version of comms aims to add a few additional steps to ensure that our packets arrive uncorrupted.


## How to use

### Initializing
```py
import numpy as np
from Comms import Comms
com = Comms()
```
### Optional specifications
The comms class is preinitialized with default robot parameters. You can optionally initialize the comms class with new parameters for quick tweaking from `main`. 
```py
def __init__(self, init_string=None, r=None, d=None, pinout=17):
```
Where `r` is the radius of the wheel, `d` is the distance between the wheels, and `pinout` is the GPIO pin indicating the status of the Arduino.



### Performing commands
This new class abstracts the following essential commands. This makes it easier to control the robot and hides the lower-level calculations. 
- Stop
- Rotate
- Linear traverse
- Circular traverse

Each require a specific set of arguments.
```py
# requires no arguments
def stop(self):

# rotate by how many degrees. In radians?
def rotate(self, angle, radians=False):

# move by what distance (this can be negative). In meters?
def linTraverse(self, distance, meters=False):
    
# the most complex of the moves. 
# radius (from center of axis) 
# direction to rotate (about the left side, or right side)
# portion, the amount of the full circle to go. this argument has not been implemeneted
def circularTraverse(self, radius, direction="left",portion=1):

```

### Reading Data
In our program, the only way to read information from the Arduino is by checking the state of a pin 10 on the Arduino. When the pin is sit to HIGH, the robot is motionless and in a neutral. When set to low, the bot is in a state of motion.


### Parameters
```py
NEUTRAL = 0x00
STOP = 0x01
SEARCH = 0x02
LINEAR_TRAVERSE = 0x03
CIRCULAR_TRAVERSE = 0x04
ROTATE = 0x05
REQUEST = 0x06
```



---
### Sending Raw Data
**WARNING:** This edition of Comms simplifies motions. Since we can't have truly private functions in python, the user can still call `_sendData()` directly, but should do so with extreme caution. 

Contruct a list such that the first element is the instruction. Every element following the instruction should be of type **float**. For most cases, you will only need to send an instruction and a single value.

In this example, we tell the bot to rotate perform a rotation where each of it's wheels should rotate pi/2 radians
```py
payload = [com.ROTATE, np.pi/2, np.pi/2] # Construct a packet
com._sendData(payload) # send data
```

**NOTE**: If you try to send data in the form of a string, or if float values are not of type float, the function call will simply return without sending any data to the arduino. 




## Packet Structure
How does the Comms class format the actual bytes payload that gets sent to the Arduino? 
This is important to know when handling incoming packets on the Arduino. 
We know from the [Sending Data](###sending-data) section that for a simple angle change, we call the ```Comms.sendData``` method with a specified packet structure. 
This method converts the instruction and floating-point values into raw bytes before sending.
The method also embeds some extra information regarding the size of the packet as well.
Such packet has the following format

Byte:
1. Instruction
2. Number of floating point values following the instruction
3. Floating-point value 1: Byte 0
4. Floating-point value 1: Byte 1
5. Floating-point value 1: Byte 2
6. Floating-point value 1: Byte 3

7. etc ...
