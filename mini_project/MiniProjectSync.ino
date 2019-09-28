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
float timeNow = 0;
const float r = .05;
const float d = 0.1;
const float pi = 3.14159;
const float tick = pi/800;
const int sampTime = 5;
float xNew = 0;
float yNew = 0;
float xOld = 0;
float yOld = 0;
float phiNew = 0;
float phiOld = 0;
float deltaThetaR = 0;
float deltaThetaL = 0;
float phiphi;
float angVel;
unsigned long time1 = 0;
int count = 0;
float error = 0.0000;
int actSignal = 0;
float cumError = 0.000;
float elapsedTime = 0.0000;
float lastTime = 0.0000;
float lastError = 0.0000;
float rateError = 0.0000;
float Kp = 48.0000;
float Ki = 21.0000;
float Kd = 7.0000;
bool direct = LOW;
Encoder knobLeft(3, 4);
Encoder knobRight(2, 5);

void setup() {
  Serial.begin(115200);
  float pid(float positionCur, float elapsedTime, float setPoint);
  pinMode(4, OUTPUT);
  digitalWrite(4, HIGH);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(12, INPUT);
}

float pid(float positionCur, float currentTime, float setPoint)
{
  Serial.print("Current Position = ");
  Serial.print(positionCur);
  Serial.print(", Current Time = ");
  Serial.print(currentTime);
  Serial.print(", Set Point = ");
  Serial.print(setPoint);
  Serial.println();
    elapsedTime = currentTime - lastTime;
    lastTime = currentTime;
    error = setPoint - positionCur;
    cumError = cumError + error * elapsedTime;
    rateError = (error - lastError)/elapsedTime;
    actSignal = (Kp * error) + (Ki * cumError) + (Kd * rateError);
    lastError = error;
    if (actSignal > 255){
      actSignal = 255;
    }
    
    Serial.print("Actuating Signal = ");
    Serial.println(actSignal);
    return actSignal;
}

void loop() {
  timeNow = millis();
  
  long newLeft, newRight;
  newLeft = knobLeft.read();
  newRight = knobRight.read();

//  
//******** PID FUNction ********//
//
  actSignal = pid(phiOld, timeNow/1000, pi);
  if(actSignal < 0){
    direct = HIGH;
  }
  if(actSignal > 0){
    direct = LOW;
  }
  
  digitalWrite(7, direct);
  analogWrite(9, abs(actSignal));

  if (newLeft != positionLeft || newRight != positionRight) 
  {

    deltaThetaR = (newRight - positionRight) * tick;
    deltaThetaL = (newLeft - positionLeft) * tick;
    xNew = xOld + cos(phiOld)*(r/2)*(deltaThetaR + deltaThetaL);
    yNew = yOld + sin(phiOld) * (r/2)*(deltaThetaR + deltaThetaL);
    phiNew = phiOld + (r/d)*(deltaThetaR - deltaThetaL);
//    Serial.print("X = ");
//    Serial.print(xNew);
//    Serial.print(", Y = ");
//    Serial.print(yNew);
//    Serial.print(", phi = ");
//    Serial.print(phiNew, 5);
//    Serial.println();
    positionLeft = newLeft;
    positionRight = newRight;
    xOld = xNew;
    yOld = yNew;
  }
  phiphi = phiOld;
  phiOld = phiNew;
  int a = phiOld * 100;
  float b = a;
  b = b/100;
  if (b >= 6.28 || b <= -6.28)
  {
    phiOld = 0;
  }
  if (Serial.available()) {
    Serial.read();
    Serial.println("Reset both knobs to zero");
    knobLeft.write(0);
    knobRight.write(0);
  }
  while(millis() < timeNow + sampTime){
  }
  
  if (phiNew != phiphi){
    angVel = (phiNew-phiphi)*1000 / sampTime;
  } else{
    angVel = 0;
  }

  
//  if (millis() >= 1000 && millis() <= 2000){
//    analogWrite(9, 100);
//    digitalWrite(7, LOW);
////    Serial.print("Angular Velocity = ");
//    Serial.print(angVel);
////    Serial.print(" rad/s");
//    Serial.println();
//    time1 = millis();
////    Serial.print("Time = ");
//    Serial.print(time1);
//    Serial.println();
//  }

}
