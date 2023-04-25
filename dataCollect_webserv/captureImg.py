import cv2
import numpy as np
import os
import threading
import re
from LEDcontrol import PiLedControll
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import sys


# gets terminal input in a non-blocking fashion
class KeyboardThread(threading.Thread):

    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            self.input_cbk(input()) #waits to get input + Return

# terminal input callback
def my_callback(inp):
    global startStop
    global exposure
    startStop = not(startStop)
    lc.set_dias(startStop)
    #evaluate the keyboard input
    print('Video running:', startStop)
    if (startStop):
        if(inp == "1"):
            exposure = 4000
            print("Exposure set for grey teeth")
        elif(inp == "2"):
            exposure = 800
            print("Exposure set for shiny teeth")
        elif(inp == "3"):
            exposure = 500
            print("Exposure set for real teeth")
        else:
            exposure = 4000
            print("Exposure set for grey teeth")



def getSampleNumber():
    fileNames = os.listdir("./img")
    lenghtOfFileNames = len(fileNames)
    
    return lenghtOfFileNames 

def myzoom(val):
    "Convert from float to tuple for camera"
    #print ("myzoom", val)
    dif =1-val
    res = (dif/2,dif/2,1-dif,1-dif)
    return res


try:
    path = "./img"
    frame_counter = getSampleNumber()
    kthread = KeyboardThread(my_callback)
    lc = PiLedControll()
    startStop = 0

    exposure = 3000
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (160, 160)
    camera.zoom = myzoom(0.8)
    #camera.framerate = 10
    # grey teeth 4000
    # shiny teeth 800
    
    rawCapture = PiRGBArray(camera, size=(160, 160))

    # allow the camera to warmup
    

    # capture frames from the camera
    #for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #    frame = frame.array

    #while cap.isOpened():
    print(startStop)
    while(1):
        camera.shutter_speed  = exposure
        while(startStop==1):
            #ret, frame = cap.read()
            #time.sleep(0.4)
            #print("START")
            
            camera.capture(f"img/{frame_counter}.png")
            #cv2.imwrite(os.path.join(path , f"{frame_counter}.png") , frame)
            #cv2.imshow(f"{frame_counter}", frame)
            frame_counter+=1
            #print(f"Number of images captured: {frame_counter}")
        
            #rawCapture.truncate(0)
        else:
            pass
                #rawCapture.truncate(0)
        #cap.release()
    #cv2.destroyAllWindows()  

except KeyboardInterrupt:
    # quit
    sys.exit()

