# this class handles the communication between RPi and Arduino
import board
import busio
import numpy as np
from smbus2 import SMBus
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import time
import struct
import threading
from subprocess import Popen, PIPE
from ..Finder.Finder import Finder
import RPi.GPIO as gpio




class Comms(object):

    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.IN)
    
    lcd = None # lcd object
    bus = None # bus obj
    address = 0
    state = 0

    # bot attributes
    r = 0.149/2 # radius of wheel
    d = 0.270 # distance between wheels (measured from center)
    
    # these constants serve as a the fist data byte in each
    # i2c tranmission packet 
    
    """ protocol """
    NEUTRAL = 0x00
    STOP = 0x01
    SEARCH = 0x02
    LINEAR_TRAVERSE = 0x03
    CIRCULAR_TRAVERSE = 0x04
    ROTATE = 0x05
    REQUEST = 0x06

    """ commands """
    commands = dict()
    commands['angle change'] = ROTATE
    commands['linear traverse'] = LINEAR_TRAVERSE
    commands['circular traverse'] = CIRCULAR_TRAVERSE
    commands['search'] = SEARCH
    commands['stop'] = STOP

 
    f = Finder()


    def __init__(self, init_string=None, r=None, d=None, pinout=17):
        
        # init lcd display
        default_message = "Creamsoup\nSuperbot AI"
        col = 16
        row = 2
        i2c = busio.I2C(board.SCL, board.SDA)
        self.lcd = character_lcd.Character_LCD_RGB_I2C(i2c, 16, 2) # proto, row, col
        self.lcd.color = [100, 100, 100]

        # set the initial default lcd display
        # TODO: a more proper check of string sizes
        if not init_string:
            self.lcd.message = default_message
        elif len(init_string) > 33:
            print('init string is to large')
            self.lcd.message = default_message
        else:
            self.lcd.message = init_string

        # init arduino bus
        self.bus = SMBus(1)
        self.address = 0x08

        self.r = r or self.r
        self.d = d or self.d
        self.state = self.NEUTRAL
        self.did_send_packet = False


        print("""Initialized Comms with the following Robot Parameters
Wheel Radius: {} m & Wheel Distance: {} m""".format(self.r, self.d))
    

    # deprecate
    def scan_state(self, timeout=15):
        print("broken function")

    # deprecate?
    def is_moving(self):
        if self.state != self.NEUTRAL:
            return False
        else:
            return True
    
    # set up functions
    def startup_color_sequence(self):
        self.set_screen_color("100 0 0")
        time.sleep(0.25)
        self.set_screen_color("0 100 0")
        time.sleep(0.25)
        self.set_screen_color("0 0 100")
        time.sleep(0.25)
        self.set_screen_color("100 100 100")

    def set_screen_color(self, rgb):
        # rgb should be a list containing the rgb values respectively
        # you can also pass a string such that -> "r g b"
        if type(rgb) == str:
            rgb = rgb.split()
        
        if len(rgb) != 3:
            print("invalid color dimensions")
            print('Use color command -> "color r g b"')
            return

        # change the screen color
        try:
            self.lcd.color = [int(i) for i in rgb]
            print("Set screen color")
        except:
            print("Error setting screen color")
        

        
    # extraneous function, future version may deprecate
    # deprecate 
    def input_handler(self, command):

        # empty string?
        if command == "":
            print("ERR: empty command")
            return

        # if not already a list, convert to it
        if type(command) != list:
            command = command.split()

        # check for keyword special arguments
        if command[0] == 'color':
            self.set_screen_color(command[1:])
                  
        elif command[0] == 'clear':
            self.lcd.clear()

    
    # deprecate
    def getData(self, val):
        if val == self.READ_ANGLE:
            response = self.bus.read_i2c_block_data(self.address, val, 4)
            b = struct.pack('BBBB', response[0],response[1],response[2], response[3])
            val = struct.unpack('f',b)
            print(val)
            return val


    def wait(self, delay=0.3, timeout=15):
        timeout = time.time() + timeout
        time.sleep(delay)
        while gpio.input(17) == False or self.did_send_packet == False:
            if time.time() > timeout:
                print("FAILED TO VERIFY MOTION TERMINATION\nEXITING")
                exit(-1) 


    # movement commands

    def search(self, direction, timeout=25, angle_delta=25):
        # try:
        timeout = time.time() + timeout
        self.f.find_markers()
        # com.search() 
        # begin serach
        while self.f.did_detect == False:
            if direction == 'r':
                self.rotate(-angle_delta)
            else:
                self.rotate(angle_delta)
        
            self.wait(delay=0.2)
            self.f.find_markers()
            # f.find_markers()
            if time.time() > timeout:
                print('Timeout')
                return False
        return True
        # except:
            # print('wack')
            # return False

    def find_closest_not_complete(self, direction, points_found, overshoot=0.2, offset=0.3048):
        if self.search(direction) == False:
            print("Could not find markers, returning")
            return False

        result = self.f.markers
        if len(result) == 0: 
            print("marker list is empty, returning")
            return False

        min_dis = 100000
        closest_id = None


        print("Found these markers", points_found)
        for i in result:
            print(i)
            if i not in points_found[1:]:
                if result[i][0] < min_dis:
                    min_dis = result[i][0]
                    closest_id = i


        distance = result[closest_id][0]/100
        angle = result[closest_id][1] * 180/np.pi
        points_found.append(closest_id)

        print("Distance {} angle {}".format(distance, angle))

        if direction == 'l':
            angle += np.arctan(offset/distance)*180/np.pi
        else:
            angle += np.arctan(offset/distance)*180/np.pi

        distance = np.sqrt(distance**2 + 0.3048**2) + overshoot

        print("Distance {} angle {}".format(distance, angle))

        return [float(distance), float(-angle), points_found]



    # # this function might be usless
    # def search(self):
    #     angle1 = 2*np.pi
    #     theta = angle1 * self.d / self.r
    #     self._sendData([self.SEARCH, float(theta), float(theta)])
    #     print('SENT SIG SEARCH')

    def stop(self):
        self._sendData([self.LINEAR_TRAVERSE, 0.0, 0.0])
        print("SENT SIG STOP")

    def rotate(self, angle, radians=False):
        # angle should come in as degrees
        if radians == False:
            angle *= np.pi/180
        theta = angle * self.d / self.r
        self._sendData([self.ROTATE, theta, theta])
        print("ROTATING WHEELS {} RADS".format(theta))


    def linTraverse(self, distance, meters=False):
        if meters == False:
            distance = distance/3.281
        theta = distance / self.r * 2.0
        payload = [self.LINEAR_TRAVERSE, float(-theta), float(theta)]
        self._sendData(payload)
        print("TRAVERSING {} meters.".format(distance))

    def circularTraverse(self, radius, direction="left",portion=1):
        # direction will usually be left if traversing
        # course counter clockwise
        # portion is the amount of circle we want to travel
        # portion=0.5 would travel a perfect half-circle

        
        payload = [self.CIRCULAR_TRAVERSE]
        shorter = 2*np.pi*(radius-self.d/2)*2
        longer  = 2*np.pi*(radius+self.d/2)*2

        if direction == "left":
            theta_l = shorter/self.r
            theta_r = longer/self.r
        elif direction == "right":
            theta_r = shorter/self.r
            theta_l = longer/self.r
        else:
            print("IMPROPER DIRECTION DEFINED")
            print('should be either "left" or "right"')

        print("l: {} r: {} radius: {}".format(theta_l, theta_r, radius))
        payload.append(float(theta_l))
        payload.append(float(theta_r))
        payload.append(float(radius))
        self._sendData(payload)

        
    # the most important
    def _sendData(self, data):
        
        self.did_send_packet = False
        payload = []

        if type(data) != list:
            print("data is not a list")
            return
            
        payload.append(len(data[1:]))
        # convert floating point values
        for float_val in data[1:]:

            if type(float_val) != float:
                print("Data element is not of type float")
                print("Send Operation aborted")
                return

            b = struct.pack('f', float_val)
            t = struct.unpack('BBBB', b)
            for byte in t:
                payload.append(byte)

        if len(payload) > 32:
            print("Attempting to send more than 32 bytes\nAborting Send")
            return

        # enter loop until packet sends succ-essfully
        while True:
            try:
                self.bus.write_i2c_block_data(self.address, data[0], payload)
                self.did_send_packet = True
                break
            except:
                print("Failed to transmit packet, did arduino crash?")
                print("attempting to send again in 0.8 sec")
                time.sleep(0.8)
                
        return



if __name__ == "__main__":


    obj = Communicator("Mini Project\nPrototyping")
    
    while True:
        command = input("Enter a command: ")
        if command == 'exit':
            break

        # first try to convert input to an int
       
        try:
            command = int(command)
        except:
            pass

        obj.input_handler(command)
    

