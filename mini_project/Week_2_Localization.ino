//////---------------------------------------------------------------------------------------------------------------------------//////
//Author: Ian Welch
//Course: SEED Lab
//Problem Description: Creating a program that will increase/decrease the rate of blinking LED's that will serve as the "gas"/"brake". 
//Secondly, creating a program that will be able to discern when turning an encoder CW or CCW.
//Code Implementation: Upload the program to the Arduino and rotate the encoder to see the output on the Serial Monitor.
//////--------------------------------------------------------------------------------------------------------------------------//////
#include <Encoder.h>

long positionLeft  = 0;
long positionRight = 0;
const float r = .05;
const float d = 0.1;
const float pi = 3.14159;
const float tick = pi/800;
float xNew = 0;
float yNew = 0;
float xOld = 0;
float yOld = 0;
float phiNew = 0;
float phiOld = 0;
float deltaThetaR = 0;
float deltaThetaL = 0;
Encoder knobLeft(3, 4);
Encoder knobRight(2, 5);

void setup() {
  Serial.begin(9600);
 
}

void loop() {
  long newLeft, newRight;
  newLeft = knobLeft.read();
 
  newRight = knobRight.read();

  if (newLeft != positionLeft || newRight != positionRight) 
  {

    deltaThetaR = (newRight - positionRight) * tick;
    deltaThetaL = (newLeft - positionLeft) * tick;
    xNew = xOld + cos(phiOld)*(r/2)*(deltaThetaR + deltaThetaL);
    yNew = yOld + sin(phiOld) * (r/2)*(deltaThetaR + deltaThetaL);
    phiNew = phiOld + (r/d)*(deltaThetaR - deltaThetaL);
    Serial.print("X = ");
    Serial.print(xNew);
    Serial.print(", Y = ");
    Serial.print(yNew);
    Serial.print(", phi = ");
    Serial.print(phiNew, 5);
    Serial.println();
    positionLeft = newLeft;
    positionRight = newRight;
    xOld = xNew;
    yOld = yNew;
    phiOld = phiNew;
    int a = phiOld * 100;
    float b = a;
    b = b/100;
    if(b == 6.28 || b == -6.28)
    {
      phiOld = 0;
    }
  }
  if (Serial.available()) {
    Serial.read();
    Serial.println("Reset both knobs to zero");
    knobLeft.write(0);
    knobRight.write(0);
  }
}
