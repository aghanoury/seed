#include <Wire.h>

// TODO: implement target changing protocol
#define WRITE_ANGLE 0x09
#define READ_ANGLE 0x0A

// DIRECTION PINS
#define left_dir_pin    8
#define right_dir_pin   7

// COMMS
byte operation = 0;
byte* packets = new byte[32]; // allocate a buffer for i2c packets

byte instruction = 0;
byte num_of_floats = 0;
float angle = 0;

void setup() {
  
   Serial.begin(250000);
   Wire.begin(8);                // join i2c bus with address #8
   Wire.onReceive(receiveEvent); // register event
   Wire.onRequest(requestEvent); // might need this later

}

void loop() {
  // put your main code here, to run repeatedly:
  delay(100);
}




// ----- COMMS -------
// WARNING: THIS FUNCTION WILL BREAK. 
// (FROM RPI) DO NOT REQUEST INFORMATION FROM ARUINO AT THIS CURRENT STATE
void requestEvent(){}
//void requestEvent(){
////  Serial.println("Enter Request");
//  if (operation == READ_ANGLE) {
//
//    long *target_pos_int = (long*) &phiOld;
//    uint8_t *float_bytes = new uint8_t[4];
//    
//    for (uint8_t i = 0; i < 4; i++){
//      float_bytes[i] = uint8_t(*target_pos_int >> (i << 3));
//    }
//    Wire.write(float_bytes, 4);
//
//    delete target_pos_int;
//    delete float_bytes;
//    
//  }
////  Serial.println("Exit Request");
//}

// handle incomding i2c packets
// rewrite this using the 
void receiveEvent() {

  // copy bytes into packets
  for (byte i = 0; Wire.available(); i++) {
    packets[i] = Wire.read();
//    Serial.println(packets[i]);
  }
  
  instruction = packets[0];
  num_of_floats = packets[1];
  angle = *(float*) &packets[2];

  for (byte i = 0; i < num_of_floats; i++){
    float val = *(float*) &packets[2+(i<<2)];
    Serial.println(val);  
  }

  


//  operation = Wire.read(); // first byte is number of floats
//  if (operation == WRITE_ANGLE) {
//    uint8_t floats = Wire.read(); // s
//   
//    // allocate memory for float bytes
//    uint8_t *float_packets = new uint8_t[floats << 2];
//  
//    for (uint8_t i = 0; Wire.available(); i++){
//      float_packets[i] = uint8_t(Wire.read());
//  //    Serial.println(float_packets[i]);
//    }
//    targetAngle = *(float*) float_packets; 
//    delete float_packets;
    
//    Serial.println(target_angle);

  
}
