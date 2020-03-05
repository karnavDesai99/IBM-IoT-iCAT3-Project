#libraries
import RPi.GPIO as GPIO
import time
from firebase import firebase
from pushbullet import Pushbullet

pb = Pushbullet("your access token provided by pushbullet")
#GPIO Mode (BOARD/BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#set GPIO direction (IN/OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#Link Firebase
firebase = firebase.FirebaseApplication('your firebase project URL', None)

def distance():
    #set Trigger yo HIGH
    GPIO.output(GPIO_TRIGGER, True)
    
    #set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    
    StartTime = time.time()
    StopTime = time.time()
    
    #save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        
    #save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    
    #time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    #multiply with the sonic speed (34300 cm/s)
    #and divide by 2, because the wave will take time to reach and reflect back
    distance = (TimeElapsed*34300)/2
    
    return distance

def upload(dist):
   data = { 'msg' : 'FULL','dist' : dist }
   firebase.post('Example-Bin-420-69', data)
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" %dist)
            if (dist <= 8.0):
                upload(dist)
                dev = pb.get_device('your device name provided by pushbullet')
                push = dev.push_note("Bin Full", "Please empty the bin")
            time.sleep(5)
            
            #Reset by pressing CTRL + C
    except KeyboardInterrupt:
	print "Measurement stopped by User"
        GPIO.cleanup()
