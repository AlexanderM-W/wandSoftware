import warnings
import serial
import time
import serial.tools.list_ports
import i2cPWM
import time
#import cv2

rasPi = True
globalHeight_offset = 35.22 #[mm] measured manually, found to be 35.70mm in cad..

if(rasPi == True):
    from picamera import PiCamera

    camera = PiCamera()
    camera.resolution = (2560,1936)
    time.sleep(1)

def takeImg(height):
    if(rasPi == True):
        captureImage = input("Do you want to take an image? y/n ")
        if (captureImage == 'y'):
            camera.capture("images/cal"+str(height)+".jpg")

arduinoID = 9025
arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if (p.vid == arduinoID)  # may need tweaking to match new arduinos
]
if not arduino_ports:
    raise IOError("No Arduino found")
if len(arduino_ports) > 1:
    warnings.warn('Multiple Arduinos found - using the first')

ser = serial.Serial(arduino_ports[0],9600)
time.sleep(2)

while(1):
    command = input("Please enter command: ")
    #file input
    if(command[:1] == "f"):
        f = open(command[2:], "r")
        for x in f:
            ser.write(str.encode(x))
            stepsMoved = ser.readline().strip().decode("ascii")
            localPose_steps = ser.readline().strip().decode("ascii")
            localPose_mm = ser.readline().strip().decode("ascii")
            print("platform move ", stepsMoved, " now at step pose ", localPose_steps, " metric pose ", localPose_mm,"mm")
            globalHeight = float(localPose_mm)+globalHeight_offset
            print("global height in mm",str(globalHeight))
            takeImg(globalHeight)   
    #help
    elif(command == "h"):
        print("f <path_to_file>")
        print("d <distance_in_mm>")
    #distance
    elif(command[:1] == "d"):
        ser.write(str.encode(command[2:]))
        time.sleep(0.1)
        stepsMoved = ser.readline().strip().decode("ascii")
        localPose_steps = ser.readline().strip().decode("ascii")
        localPose_mm = ser.readline().strip().decode("ascii")
        print("platform move", stepsMoved, " now at step pose", localPose_steps, " metric pose", localPose_mm, "mm")
        globalHeight = float(localPose_mm)+globalHeight_offset
        print("global height in mm",str(globalHeight))
        takeImg(globalHeight)
    #calibrate
    elif(command == "calibrate"):
        ser.write(str.encode(command))
        time.sleep(0.1)
        line = ser.readline()
        print(line)
    #light
    elif(command[:5] == "light"):
        if(rasPi == True):
            i2cPWM.setDias(int(command[6:]))
    else:
        print("MISREAD: ",command)
