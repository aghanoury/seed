import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import time
from subprocess import Popen, PIPE

lcd_columns = 16
lcd_rows = 2
i2c = busio.I2C(board.SCL, board.SDA)
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

lcd.color = [100, 100, 100]
lcd.message = "Creamsoup"
time.sleep(3)

while(True):
    lcd.clear()
    try:
        p1 = Popen(['hostname', '-I'], stdout=PIPE)
        the_ip = p1.communicate()[0].decode('utf-8').replace('\n','')
        lcd.message = the_ip
        break
    except:
        the_ip = 'CANNOT GET\nIP'
        print("Failed to get inet")
        print("attempting to find again in 1 second")
        time.sleep(1)

