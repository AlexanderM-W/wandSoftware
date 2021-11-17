#include <Arduino.h>

// Motor steps per revolution. Most steppers are 200 steps or 1.8 degrees/step
#define MOTOR_STEPS 20
#define RPM 120
#define PITCH 0.4

#define DIR 8
#define STEP 9
#define SLEEP 13 // optional (just delete SLEEP from everywhere if not used)

#include "DRV8834.h"
#define M0 10
#define M1 11
DRV8834 stepper(MOTOR_STEPS, DIR, STEP, SLEEP, M0, M1);

double pose = 0;

void setup() {
    pinMode(7, INPUT_PULLUP);
    Serial.begin(9600);
    stepper.begin(RPM);
    stepper.disable();
    delay(1000);
}

double mmToSteps(double mm){
  return 1.0/(0.4/(20.0*mm));
}
double stepsToMm(double steps){
  return 0.4*steps/20.0;
}
void loop() {
    double distance = 0.0;
    String distance_string = "x"; 
    double steps = 0;
    if(Serial.available()>0){
      //distance = Serial.parseFloat();
      String distance_string = Serial.readString();
      if(distance_string == "calibrate"){
        while(digitalRead(7)){
          stepper.enable();
          delay(10);
          stepper.setMicrostep(1);
          steps = mmToSteps(distance);
          stepper.move(10);
        }
        pose = 0;
        distance_string = "";
        Serial.println("Jig has been calibrated");  
      }else{
        distance = distance_string.toFloat();
        if((int)(distance*100) % (int)(0.02*100) == 0 && distance != 0.0){ //check if valid step
          stepper.enable();
          delay(10);
          stepper.setMicrostep(1);  // Set microstep mode to 1:1
          delay(10);
          steps = mmToSteps(distance);
          stepper.move(steps);    // forward revolution
          //clear serial buffer
          while (Serial.available() > 0) {
            Serial.read();
          }       
          pose = pose + steps;
          //python scripts reads 3 lines
          Serial.println(steps);
          Serial.println(pose);
          Serial.println(stepsToMm(pose));
          stepper.disable();
        }
        else{
          Serial.println("Please enter a value where VAL%0.02=0");
        }
      }
    }
}
