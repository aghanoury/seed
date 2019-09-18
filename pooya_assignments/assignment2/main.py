import board
import busio
from smbus2 import SMBus
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import time
from subprocess import Popen, PIPE

# init lcd screen
lcd_columns = 16
lcd_rows = 2
i2c = busio.I2C(board.SCL, board.SDA)
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

# set the LCD screen color to white 
# not PWM, anything greater than 1 turns that color channel completely on
lcd.color = [100, 100, 100]
lcd.message = "I2C Trash"


# for RPI version 1, use “bus = smbus.SMBus(0)”
# init i2c bus
bus = SMBus(1)
address = 0x08 #arduino address

# this function handles user data meant for sending
# we are using the i2c starting index value as a psuedo header
# so the arduino can know what kind of value is being sent

def sendToDuino(data):
    
    # if the data is an integer, send a single byte
    if isinstance(data, int):
        bus.write_byte_data(address, 0, data) 
        response = bus.read_byte_data(address,2)
        print("Response:", response)
        # write message to lcd
        lcd.clear()
        lcd.message = "sent: {}\ngot: {}".format(data, response)

    # if the incoming data is a string
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


while True:
    var = input("Enter an int or string: ")

    # check for command inputs
    if var == 'color':
        color = input("Enter a sequence of rgb values: ")
        color = color.split(' ')
        color_vals = [int(i) for i in color]
        lcd.color = color_vals

    elif var == 'clear':
        lcd.clear()
    elif var == 'exit':
        exit()

    # else: processes generic input
    else:
        #attempt conversion to int, otherwise send out string
        try:
            data = int(var)
        except:
            data = var

        # send data out
        sendToDuino(data)
    
    
