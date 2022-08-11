from flask import Flask, redirect, url_for, render_template, request
import sys
import stepperTest
import IO
import threading
import time
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

app = Flask(__name__)



@app.route('/error/')
def error():
   return "An error occurred. Please try again."

@app.route('/moveStepper_mm/<up_or_down>/<mm>/')
def moveStepper(up_or_down, mm):
   stepper.moveStepper(up_or_down, stepper.mm2steps(float(mm)))
   return str(stepper.getCurrentHeight_mm())

#@app.route('/moveStepper_mm')
#def moveStepper():
#   return render_template("./moveStepper_mm.html")

@app.route('/go2pose_mm/<pose_mm>')
def go2pose_mm(pose_mm):
   stepper.go2pose_mm(pose_mm)
   return str(stepper.getCurrentHeight_mm())
   
@app.route('/calibrate/')
def hello_guest():
   stepper.calibrate()
   return str(stepper.getCurrentHeight_mm())

@app.route('/getCurrentHeight_mm/')
def getCurrentHeight_mm():
   return str(stepper.getCurrentHeight_mm())

@app.route('/')
def index():
   return render_template("./index.html")

@app.route('/',methods=['POST'])
def index_post():
   slider = request.form['slider']
   return str(slider)

def testButton1(io, stepper):
   while(1):
      #print(f"Button1 clicked {io.readButton1()}")
      if(io.readButton1()):
         stepper.moveStepper("down",50)
         if(GPIO.input(io.SW1)==GPIO.LOW):
            stepper.calibrate()
      time.sleep(0.01)

stepper = stepperTest.Stepper()
io = IO.IO(stepper)

if __name__ == '__main__':
   thread = threading.Thread(target=testButton1, args=(io,stepper,))
   #thread.daemon = True         # Daemonize 
   thread.start()
   app.run(debug = True, host = "0.0.0.0")