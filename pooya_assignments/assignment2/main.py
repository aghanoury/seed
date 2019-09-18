import board
import busio
from smbus2 import SMBus
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import time
from subprocess import Popen, PIPE

lcd_columns = 16
lcd_rows = 2
i2c = busio.I2C(board.SCL, board.SDA)
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

lcd.color = [100, 100, 100]
lcd.message = "I2C=Trash"




# for RPI version 1, use “bus = smbus.SMBus(0)”
bus = SMBus(1)
# This is the address we setup in the Arduino Program
address = 0x08

def sendToDuino(data):
    if isinstance(data, int):
        bus.write_byte_data(address, 0, data)
        response = bus.read_byte_data(address,2)
        print(response)
        lcd.clear()
        lcd.message = "sent: {}\ngot: {}".format(data, response)
    elif isinstance(data, str):
        if data == 'pot':
            response = bus.read_i2c_block_data(address, 3, 2)
            # print(response)
            value = (response[0] << 8) + response[1]
            value = round(value/1023 * 5, 2)
            lcd.clear()
            lcd.message = str(value) + ' V'
            return
        try:
            byte_array = [ord(i) for i in data]
            bus.write_i2c_block_data(address, 1, byte_array)
            time.sleep(0.1)
            response = bus.read_i2c_block_data(address, 2, len(byte_array))
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

    if var == 'color':
        color = input("Enter a sequence of rgb values: ")
        color = color.split(' ')
        color_vals = [int(i) for i in color]
        lcd.color = color_vals

    elif var == 'clear':
        lcd.clear()
    elif var == 'exit':
        exit()
    elif var == 'pot':
        sendToDuino(var)
    else:
        try:
            data = int(var)
        except:
            data = var

        sendToDuino(data)
        
        # try:
        #     data = int(var)
        #     sendToDuino(data) # if entered int, write int
        # except:
        #     print("1111111111111")
        #     sendToDuino(var) # if enetered string, send string
    
    
    
