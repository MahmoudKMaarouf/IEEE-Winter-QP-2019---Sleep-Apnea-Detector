import pyaudio
import wave
import os
import lcd_i2c
import switch
import sys
import time

CHUNK = 4096 #1024 supposed to be 1600
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "RECORDINGS/output"
dev_index = 2


if (switch.state()==1):
    lcd_i2c.cancel()
    time.sleep(2)
    os.system('python start.py')


    
r = 0
x = 6 #NUMBER OF RECORDINGS 
while (r<x): #NUMBER OF RECORDINGS 
    
    if (switch.state()==1):
        lcd_i2c.cancel()
        time.sleep(2)
        os.system('python start.py')

    
    
    lcd_i2c.rec(r,x)
    
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                input_device_index = dev_index,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
    print("* recording "+str(r))
    
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK,exception_on_overflow = False)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME+str(r)+".wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    r = r+1

if (switch.state()==1):
    lcd_i2c.cancel()
    time.sleep(2)
    os.system('python start.py')

lcd_i2c.rec(r,x)
os.system('python example.py')