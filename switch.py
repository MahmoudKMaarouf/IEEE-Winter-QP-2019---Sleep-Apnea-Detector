import RPi.GPIO as GPIO
import time
import subprocess


def state():
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    input_state = GPIO.input(26)
    return input_state 

