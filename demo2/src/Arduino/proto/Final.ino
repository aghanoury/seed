//////---------------------------------------------------------------------------------------------------------------------------//////
//Author: Ian Welch, Dan McElroy, Pooya Aghanoury, Jason Matney
//Course: SEED Lab
//Problem Description: Execute command and control from raspberry pi. 

#include <Encoder.h>
#include <Wire.h>


// 

// TODO: implement target changing protocol
#define WRITE_ANGLE 0x09
#define READ_ANGLE 0x0A

// DIRECTION PINS
#define left_dir_pin    4
#define right_dir_pin   5

// with this, we can assign directions to the motors
// EX: left_motor_direction = backward; // assigns backward (int 0) 
// EX: cout << left_motor_direction << endl; // would print '0'
enum WheelDirection {forward = 1, backward = 0};
WheelDirection left_motor_direction = forward;
WheelDirection right_motor_direction = forward;



// COMMS
byte operation = 0;
byte* packets = new byte[32]; // allocate a buffer for i2c packets




// USEFUL CONSTANTS (USEFUL FACTS)
const float r = .05;
const float d = 0.1;
const float pi = 3.14159;

const int ticks_per_rot = 1600; // num of ticks in a full 360 rotation 
const float tick_rad = pi/800; // rads corresponding to a single tick
const float tick_deg = 0.225; // degrees corresponding to a single tick

// TIME
float timeNow = 0; // captures millis() at beginning of each loop
float lastTime = 0; // store previous "timeNow" value

// POSITION
float xNew = 0;
float yNew = 0;
float xOld = 0;
float yOld = 0;
float phiNew = 0;
float phiOld = 0;
float deltaThetaR = 0;
float deltaThetaL = 0;
float phiphi;
long positionLeft  = 0;
long positionRight = 0;

// CONTROLS
float angVel; // angular velocity of...? might need
float cumError = 0; // speaks for itself
float elapsedTime = 0; 
float lastError = 0;
float rateError = 0;
float Kp = 100.0;
float Ki = 21.0;
float Kd = 7.0;
float error = 0;
int actSignal = 0; // what is this used for?


// MOTOR ENCODERS. Pins 2 and 3 are interrupt pins.//
Encoder knobLeft(3, 4);
Encoder knobRight(2, 5);

float targetAngle = 270;

// FUNCTION DECLARATIONS
float pid(float, float, float); // PID
void requestEvent();
void receiveEvent();


void setup() {
  Serial.begin(250000);
  
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
//TODO: convert this controller to work with milliseconds
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
  timeNow = millis(); // grab current time
  
  
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

    deltaThetaR = (newRight - positionRight) * tick_rad;
    deltaThetaL = (newLeft - positionLeft) * tick_rad;
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

  //rollover after full rotation
  if (b >= 360 || b <= -360)
  {
    phiOld = 0;
  }


}


// ----- COMMS -------
// WARNING: THIS FUNCTION WILL BREAK. 
// (FROM RPI) DO NOT REQUEST INFORMATION FROM ARUINO AT THIS CURRENT STATE
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

// handle incomding i2c packets
// rewrite this using the 
void receiveEvent() {

  
  
  operation = Wire.read(); // first byte is number of floats
  if (operation == WRITE_ANGLE) {
    uint8_t floats = Wire.read(); // s
   
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
