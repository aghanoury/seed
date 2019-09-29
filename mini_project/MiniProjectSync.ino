//////---------------------------------------------------------------------------------------------------------------------------//////
//Author: Ian Welch
//Course: SEED Lab
//Problem Description: Creating a program that will increase/decrease the rate of blinking LED's that will serve as the "gas"/"brake". 
//Secondly, creating a program that will be able to discern when turning an encoder CW or CCW.
//Code Implementation: Upload the program to the Arduino and rotate the encoder to see the output on the Serial Monitor.
//////--------------------------------------------------------------------------------------------------------------------------//////
#include <Encoder.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

//LiquidCrystal_I2C lcd(0x20, 16, 2);

// TODO: implement target changing protocol
#define WRITE_ANGLE 0x09
#define READ_ANGLE 0x0A
// COMM globals
uint8_t operation = 0;

long positionLeft  = 0;
long positionRight = 0;
float timeNow = 0;
const float r = .05;
const float d = 0.1;
const float pi = 3.14159;
// Variable for encoder positions. One full rotation of encoder is 1600 ticks.//
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
float error = 0;
int actSignal = 0;
float cumError = 0;
float elapsedTime = 0;
float lastTime = 0;
float lastError = 0;
float rateError = 0;
float Kp = 100.0;
float Ki = 21.0;
float Kd = 7.0;
// Variable for motor direction //
bool direct = LOW;
// Setting up Arduino pins for encoders. Pins 2 and 3 are interrupt pins.//
Encoder knobLeft(3, 4);
Encoder knobRight(2, 5);

float targetAngle = 3*pi/2;



void setup() {
  Serial.begin(250000);
  float pid(float positionCur, float elapsedTime, float setPoint);
  pinMode(4, OUTPUT);
  digitalWrite(4, HIGH);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(12, INPUT);


  Wire.begin(8);                // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // register event
  Wire.onRequest(requestEvent); // might need this later

//  lcd.init();
//  lcd.backlight();
//  lcd.setCursor(0,0);
//  lcd.print("Trash");

}
//
//
////////////////////////// Function for the motor controller //////////////////////////
// 
//
float pid(float positionCur, float currentTime, float setPoint)
{
//  Serial.print("Current Position = ");
//  Serial.print(positionCur);
//  Serial.print(", Current Time = ");
//  Serial.print(currentTime);
//  Serial.print(", Set Point = ");
//  Serial.print(setPoint);
//  Serial.println();
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
    
//    Serial.print("Actuating Signal = ");
//    Serial.println(actSignal);
    return actSignal;
}

void loop() {
  timeNow = millis();
  
  long newLeft, newRight;
  newLeft = knobLeft.read();
  newRight = knobRight.read();

//  
//********************              Calling PID FUNction         *********************//
//
  actSignal = pid(phiOld, timeNow/1000, targetAngle);
  if(actSignal < 0){
    direct = HIGH;
  }
  if(actSignal > 0){
    direct = LOW;
  }
  //// digitalWrite sets pin 7 HIGH or LOW for rotation direction and analogWrite sets pin 9 for PWM duty cycle value ///////
  digitalWrite(7, direct);
  analogWrite(9, abs(actSignal));
//
///// this statement computes positional and rotational data
//
  if (newLeft != positionLeft || newRight != positionRight) 
  {

    deltaThetaR = (newRight - positionRight) * tick;
    deltaThetaL = (newLeft - positionLeft) * tick;
    xNew = xOld + cos(phiOld)*(r/2)*(deltaThetaR + deltaThetaL);
    yNew = yOld + sin(phiOld) * (r/2)*(deltaThetaR + deltaThetaL);
    phiNew = phiOld + (r/d)*(deltaThetaR - deltaThetaL);
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
  ///// This waits for a set amount of time (sampTime) and computes angular veloctiy////
  while(millis() < timeNow + sampTime){
  }
  
  if (phiNew != phiphi){
    angVel = (phiNew-phiphi)*1000 / sampTime;
  } else{
    angVel = 0;
  }
}


// ----- COMMS -------
void requestEvent(){
//  Serial.println("Enter Request");
  if (operation == READ_ANGLE) {

    long *target_pos_int = (long*) &phiOld;
    uint8_t *float_bytes = new uint8_t[4];
    
    for (uint8_t i = 0; i < 4; i++){
      float_bytes[i] = uint8_t(*target_pos_int >> (i << 3));
    }
    Wire.write(float_bytes, 4);

    delete target_pos_int;
    delete float_bytes;
    
  }
//  Serial.println("Exit Request");
}

void receiveEvent() {
//  Serial.println("Enter Receive");
   // first byte is number of floats
  operation = Wire.read();
  if (operation == WRITE_ANGLE) {
    
    // second byte is operation
    uint8_t floats = Wire.read();
   
    // allocate memory for float bytes
    uint8_t *float_packets = new uint8_t[floats << 2];
  
    for (uint8_t i = 0; Wire.available(); i++){
      float_packets[i] = uint8_t(Wire.read());
  //    Serial.println(float_packets[i]);
    }
    targetAngle = *(float*) float_packets; 
    delete float_packets;
    
//    Serial.println(target_angle);
  }
  
}
