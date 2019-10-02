// The purpose of this file is to test converting
// floating point numbers into 4 raw bytes

#include <iostream>
#include "inttypes.h"

using namespace std;

int main() {


    uint8_t packets[4] = {219, 15, 73, 64};

    float *angle = (float*) packets;  // optionally could also be &packets
    // float angle = *(float*) packets; // this could also work
    cout << "Converting from raw byes into a float: " << *angle << endl;

    float np_angle = *angle;
    // convert from float to bytes
    uint8_t* np_packets = new uint8_t[4];
    np_packets = (uint8_t*) &np_angle; // or could use "angle" as it is already a pointer

    cout << "Converting from float to raw bytes: ";
    for (int i = 0; i < 4; i++){
        cout << (int) np_packets[i] << " ";
    }
    cout << endl;

    return 0;

}