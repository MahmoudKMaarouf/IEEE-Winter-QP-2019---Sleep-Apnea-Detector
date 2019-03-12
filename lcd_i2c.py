#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#  lcd_i2c.py
#  LCD test script using I2C backpack.
#  Supports 16x2 and 20x4 screens.
#
# Author : Matt Hawkins
# Date   : 20/09/2015
#
# http://www.raspberrypi-spy.co.uk/
#
# Copyright 2015 Matt Hawkins
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#--------------------------------------
import smbus
import time

# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address
LCD_WIDTH = 20   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def main():
    
  # Main program block

  # Initialise display
    lcd_init()

    while True:

    # Send some test
        lcd_string(" glitch2",LCD_LINE_1)
        lcd_string(" GLITCH???/",LCD_LINE_2)
        lcd_string(" ",LCD_LINE_3)

        time.sleep(3)
  
    # Send some more text
        lcd_string("glitch3 ",LCD_LINE_1)
        lcd_string(" ",LCD_LINE_2)
        lcd_string(" ",LCD_LINE_3)


        time.sleep(3)
    
if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)


    
def rec(r,x):
  
    lcd_init()
    
    lcd_string("Recording...",LCD_LINE_1)
    lcd_string(" ",LCD_LINE_2)
    lcd_string(" ",LCD_LINE_3)
    lcd_string("Progress:   " + str((r*100/x))+"%",LCD_LINE_4)
    
def connect():
  
    lcd_init()
    
    lcd_string(" ",LCD_LINE_1)
    lcd_string("Connecting to MYSQL ",LCD_LINE_2)
    lcd_string("database... ",LCD_LINE_3)
    lcd_string(" ",LCD_LINE_4)
    time.sleep(2)
    
def scan(r,x,conf):
  
    lcd_init()
    
    lcd_string("Analyzing wav ",LCD_LINE_1)
    lcd_string("files... ",LCD_LINE_2)
    lcd_string("Confidence: "+str(conf),LCD_LINE_3)
    lcd_string("Progress:   " + str((r*100/x))+"%",LCD_LINE_4)
    
def wait():
  
    lcd_init()
    lcd_string("Progress:   " + "100%",LCD_LINE_4)
    lcd_string("Detecting sleep",LCD_LINE_1)
    lcd_string("apnea...",LCD_LINE_2)
    lcd_string(" ",LCD_LINE_3)
    time.sleep(3)
    
def resultneg():
    
    lcd_init()
    
    lcd_string("Negative",LCD_LINE_1)
    lcd_string("",LCD_LINE_2)
    lcd_string("No sleep apnea signs",LCD_LINE_3)
    lcd_string("detected.",LCD_LINE_4)
    
def resultpos():
    
    lcd_init()
    
    lcd_string("**POSITIVE**",LCD_LINE_1)
    lcd_string("",LCD_LINE_2)
    lcd_string("Sleep apnea signs",LCD_LINE_3)
    lcd_string("detected.",LCD_LINE_4)
    
    
def fingerprint():
    
    lcd_init()
    
    lcd_string("Fingerprinting",LCD_LINE_1)
    lcd_string("database",LCD_LINE_2)
    lcd_string("directory...",LCD_LINE_3)
    lcd_string("",LCD_LINE_4)
    
def off():
    
    lcd_init()
    lcd_string("Flip switch to",LCD_LINE_3)
    lcd_string("activate program.",LCD_LINE_4)
    
def on():
    
    lcd_init()
    
    lcd_string("Activating",LCD_LINE_1)
    lcd_string("program...",LCD_LINE_2)
    lcd_string("",LCD_LINE_3)
    lcd_string("",LCD_LINE_4)

    
def cancel():
    
    lcd_init()
    
    lcd_string("XXXXXXXXXXXXXXXXXXXX",LCD_LINE_1)
    lcd_string("Program",LCD_LINE_2)
    lcd_string("terminated",LCD_LINE_3)
    lcd_string("XXXXXXXXXXXXXXXXXXX",LCD_LINE_4)
    
def reset():
    
    lcd_init()
    
    lcd_string("Reseting ",LCD_LINE_1)
    lcd_string("program...",LCD_LINE_2)
    lcd_string("",LCD_LINE_3)
    lcd_string("",LCD_LINE_4)

    
    
    
    

    
