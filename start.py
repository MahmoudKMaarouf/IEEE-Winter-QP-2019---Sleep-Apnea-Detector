import RPi.GPIO as GPIO
import time
import subprocess
import lcd_i2c
import os
import sys

GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lcd_i2c.off()

while True:
    print("switch off")        # block until finished (depending on application)
    time.sleep(1)
    input_state = GPIO.input(26)
    if input_state == False:
        lcd_i2c.on()
        print("switch on")        # block until finished (depending on application)
        time.sleep(2)
        os.system('python micrecord.py')
        sys.exit()

        
