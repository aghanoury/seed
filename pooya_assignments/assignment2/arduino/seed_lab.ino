#include <Wire.h>


int analogPin = A2;
uint16_t pot_value = 0;
uint8_t pot_regs[2]= {0};


// globals

// allocate an array of 100 bytes 
uint8_t c[100] = {0};
int payload_size = 0;
int global_payload_size = 0;
uint8_t buff[100] = {0};
uint8_t return_sum = 0;
char return_mode = 'n';



void setup() {
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // register event
  Wire.onRequest(requestEvent);
//  Serial.begin(9600);
}

void loop() {
  pot_value = analogRead(analogPin);
  pot_regs[0] = pot_value >> 8;
  pot_regs[1] = pot_value;
//  Serial.print(pot_regs[0]);
//  Serial.print(' ');
//  Serial.println(pot_regs[1]);
}

// function that executes whenever data is requested by master
// this function is registered as an event, see setup()
void receiveEvent() {
  
  int i = 0;
  int header = Wire.read();
  payload_size = Wire.available();
 
  
  if (header == 0) {
    return_mode = 's';
    return_sum = Wire.read() + 5;
  }
  else if (header == 1) {
    return_mode = 'a';
    
    while(Wire.available()) {
      c[i] = uint8_t(Wire.read());  
//      Serial.println(c[i]);
      i++;
    }
    global_payload_size = payload_size;
  }
  else if(header == 2) return;
  else if(header == 3) {
    c[0] = pot_value >> 8;
    c[1] = pot_value;
    global_payload_size = 2;
    return_mode = 'v';
  }


  
//  Serial.println("---------------");

}

void requestEvent() {
//  Serial.println(return_mode); 
  if (return_mode == 'n') return;
  //for single bytes
  else if (return_mode == 's') {
    Wire.write(return_sum);
  }
  else if (return_mode == 'a') {

    uint8_t tmp_buff[global_payload_size];
    for (int i = 0; i < global_payload_size; i++) {
       tmp_buff[i] = c[global_payload_size - 1 - i];
//       Serial.println(c[i]);
    }
    Wire.write(tmp_buff, global_payload_size);
  }
  else if (return_mode == 'v') {
    uint8_t tmp_buff[global_payload_size];
    for (int i = 0; i < global_payload_size; i++) {
       tmp_buff[i] = c[i];
//       Serial.println(c[i]);
    }
    Wire.write(tmp_buff, global_payload_size);
  }
  
  global_payload_size = 0;
//  Serial.println("Responded");
}
