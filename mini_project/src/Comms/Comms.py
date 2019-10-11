# this class handles the communication between RPi and Arduino
import board
import busio
from smbus2 import SMBus
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import time
import struct
from subprocess import Popen, PIPE

class Comms(object):
    
    lcd = None # lcd object
    bus = None # bus obj
    address = 0

    # these constants serve as a the fist data byte in each
    # i2c tranmission packet 
    
    """ protocol """
    CHANGE_POS = 0x03
    WRITE_ANGLE = 0x09
    READ_ANGLE = 0x0A


    def __init__(self, init_string=None):
        
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



    def startup_color_sequence(self):
        self.set_screen_color("100 0 0")
        time.sleep(0.5)
        self.set_screen_color("0 100 0")
        time.sleep(0.5)
        self.set_screen_color("0 0 100")
        time.sleep(0.5)
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

    

    def getData(self, val):
        if val == self.READ_ANGLE:
            response = self.bus.read_i2c_block_data(self.address, val, 4)
            b = struct.pack('BBBB', response[0],response[1],response[2], response[3])
            val = struct.unpack('f',b)
            print(val)
            return val


    # the most important
    def sendData(self, data):
        
        payload = []

        if type(data) != list:
            print("data is not a string")
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

        # print(payload)
        try:
            self.bus.write_i2c_block_data(self.address, data[0], payload)
        except:
            print("Failed to transmit packet, did arduino crash?")
        # time.sleep(1)
        # response = self.bus.read_i2c_block_data(self.address, data[0]+1, 4)
        # b = struct.pack('BBBB', response[0],response[1],response[2], response[3])
        # val = struct.unpack('f',b)
        # print(val)
        # self.getData(self.READ_ANGLE)
        
        return





        """ Deprecated below """
        if isinstance(data, int):
            self.bus.write_byte_data(self.address, 0, data) 
            response = self.bus.read_byte_data(self.address,2)
            print("Response:", response)
            # write message to lcd
            self.lcd.clear()
            self.lcd.message = "sent: {}\ngot: {}".format(data, response)


        elif isinstance(data, str):

            # requesting for pot?
            if data == 'pot':
                # make a read request with header of 3
                response = bus.read_i2c_block_data(address, 3, 2)

                # we expect to get two bytes back. 
                # first is upper byte 16-bit analog reading
                # next is lower byte
                value = (response[0] << 8) + response[1]
                value = round(value/1023 * 5, 2)

                # write to lcd
                lcd.clear()
                lcd.message = str(value) + ' V'
                return
            try:
                byte_array = [ord(i) for i in data]
                bus.write_i2c_block_data(address, 1, byte_array)
                time.sleep(0.1)
                response = bus.read_i2c_block_data(address, 2,len(byte_array))
                payload = ''
                for i in response:
                    payload += chr(i)
            except:
                print("Failed to do something useful")
                payload = 'Failed to send/receive'
                
            lcd.clear()
            lcd.message = payload
            # except:
        

        print("sendData Function not fully implemeneted yet")



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
    



    # obj.input_handler(command)

    # # for RPI version 1, use “bus = smbus.SMBus(0)”
    # # init i2c bus
    # bus = SMBus(1)
    # address = 0x08 #arduino address

    # # this function handles user data meant for sending
    # # we are using the i2c starting index value as a psuedo header
    # # so the arduino can know what kind of value is being sent

    # def sendToDuino(data):
        
    #     # if the data is an integer, send a single byte
        

    #     # if the incoming data is a string
    #     


    # while True:
    #    

    #     # check for command inputs
    #     
    #     elif var == 'exit':
    #         exit()

    #     # else: processes generic input
    #     else:
    #         #attempt conversion to int, otherwise send out string
    #         try:
    #             data = int(var)
    #         except:
    #             data = var

    #         # send data out
    #         sendToDuino(data)
        
        
