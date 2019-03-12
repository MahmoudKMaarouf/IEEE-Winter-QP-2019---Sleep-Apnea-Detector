import warnings
import json
import lcd_i2c
import switch
import sys
import time
import os
warnings.filterwarnings("ignore")

from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer

# load config from a JSON file (or anything outputting a python dictionary)
with open("dejavu.cnf.SAMPLE") as f:
    config = json.load(f)

if __name__ == '__main__':

        if (switch.state()==1):
            lcd_i2c.cancel()
            time.sleep(2)
            os.system('python start.py')

	# create a Dejavu instance
	djv = Dejavu(config)
  
        lcd_i2c.fingerprint()
        
	# Fingerprint all the mp3's in the directory we give it    #DATABASE.   sleep apnea database here
	djv.fingerprint_directory("database", ["wav"])
	
	
	lcd_i2c.connect()

	

	# Recognize audio from a file
	
	conf_array = [0] * 300    #number of elements in array
        #print (array[99])
	r = 0
	x = 6#Number of scans
	
	
	
	while(r<x):   #Number of scans
            if (switch.state()==1):
                lcd_i2c.cancel()
                time.sleep(2)
                os.system('python start.py')
                
            if(r==0):
                lcd_i2c.scan(r,x,conf_array[r])
            else:
                lcd_i2c.scan(r,x,conf_array[r-1])


            print "Scanning output"+str(r)
            song = djv.recognize(FileRecognizer, "RECORDINGS/output"+str(r)+".wav")    #SINGLE WAV FILE WE WANT TO COMPARE TO DATABASE (Sleeping recordings here)
            try:
                song_conf = song['confidence']
                if (song_conf >= 0):
                    conf_array[r] = song_conf
            except:
                print("No attribute: confidence")
            

            
            #print(song['confidence']+100)
            
            print "From file we recognized: %s\n" % song
            r=r+1
        
        
        
        
        
        if (switch.state()==1):
            lcd_i2c.cancel()
            time.sleep(2)
            os.system('python start.py')

        lcd_i2c.wait()
        
        
        count = 0
    
        for i in range(r):
            if (conf_array[i]>19):
                count = count+1
            print(conf_array[i])
            
        if (count>2):
            lcd_i2c.resultpos()
        else:
            lcd_i2c.resultneg()


        
        while True:
            if (switch.state()==1):
                lcd_i2c.reset()
                time.sleep(2)
                os.system('python start.py')
        
	#song = djv.recognize(FileRecognizer, "RECORDINGS/none.wav")    #SINGLE WAV FILE WE WANT TO COMPARE TO DATABASE (Sleeping recordings here)
	#print "From file we recognized: %s\n" % song 

        #song = djv.recognize(FileRecognizer, "RECORDINGS/output1.wav")    #SINGLE WAV FILE WE WANT TO COMPARE TO DATABASE (Sleeping recordings here)
	#print "From file we recognized: %s\n" % song
	
       
       ## print song.__init__.largest_count
       
       
       
       
       
       # Or recognize audio from your microphone for `secs` seconds
	#secs = 5
	#song = djv.recognize(MicrophoneRecognizer, seconds=secs)
	#if song is None:
	#	print "Nothing recognized -- did you play the song out loud so your mic could hear it? :)"
	#else:
	#	print "From mic with %d seconds we recognized: %s\n" % (secs, song)

	# Or use a recognizer without the shortcut, in anyway you would like
	#recognizer = FileRecognizer(djv)
	##song = recognizer.recognize_file("mp3/Josh-Woodward--I-Want-To-Destroy-Something-Beautiful.mp3")
	#print "No shortcut, we recognized: %s\n" % song
	