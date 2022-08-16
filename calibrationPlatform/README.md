# Documentation

## Client
The client folder holds 3 subdirectories pictures_noLight, pictures_flash and pictures_dias and a python script called client.py. Before running the script the user needs to alter the IP address of both the calibration platform and the wand on line 13 and 14. The script automatically connects to both the wand and calibration platform, and prompts the user with the following:

    1: Calibrate 
    2: Get current pose
    3: Move stepper x mm in y direction 
    4: Go to pose x in mm 
    5: Take a picture 
    6: Move n steps with x mm spacing and capture images

The above options are explained below
1. Calibrates the scanner and takes no arguments.
2. Displays the current global pose of the target bed and takes no arguments.
3. Takes 2 arguments, the amount of travel and the direction to travel in. The client program further prompts the user and instructs the user on what to input when.
4. Takes 1 argument which is the desired global pose of the target bed.
5. Takes 1 argument which is the desired name of the picture. It then proceeds to capture 3 images, 1 with no lighting, 1 with flash and with with DIAS and saves them in the designated folders.
6. Takes 3 arguments, a global start pose, a global end pose and step travel. The client program further prompts the user and instructs the user on what to input when with relevant text as guide. 

## Server
The server folder holds 4 scripts and some directories used by flask. The disableStepper_boot.sh should run at startup as it ensures that the stepper is software disabled. Otherwise the stepper is always on and consumes power. The IO.py is a library file and contains an IO class which provides an interface to various buttons and endstops. It also configures an interrupt routine for the endstop switch used in the calibration of the device. The stepperLib.py is also a library that contains a Stepper class. It provides an interface to the stepper as well as various usefull functions.
The webServer.py ties everything together and is started on boot. It listens for request on following URL's

1. calibrationIP/moveStepper_mm/<up_or_down>/<mm>/
  - Moves the stepper <up_or_down> should be either "up" or "down" and mm is capped at 55mm or whenever the calibration endstop is engaged
2. calibrationIP/go2pose_mm/<pose_mm>/
  - Moves the target bed to a desired global pose, if <pose_mm> is above 55mm the target bed will not move 
3. calibrationIP/calibrate/
  - Calibrate the stepper
4. calibrationIP/getCurrentPose_mm/
  - Return the current global pose in mm.
5. calibrationIP/
  - Displays the index file, which is empty

