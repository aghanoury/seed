# this class handles the communication between RPi and Arduino
import board
import busio
from smbus2 import SMBus
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import time
from subprocess import Popen, PIPE

class Communicator(object):
    
    lcd = None # lcd object
    bus = None # bus obj
    address = 0

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

    def input_handler(self, command):

        if command == 'color':
            color = input("Enter a sequence of rgb values: ")
            color = color.split(' ')
            color_vals = [int(i) for i in color]
            self.lcd.color = color_vals

        elif command == 'clear':
            self.lcd.clear()


        if isinstance(command, int):
            print("create integer handler")

        elif isinstance(command, str):
            print("create string handler")

        elif isinstance(command, list):


    def sendData(self,data):
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

        obj.input_handler(command)

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
        
        
