#include <iostream>
#include "inttypes.h"

using namespace std;

int main() {

    uint8_t packets[4] = {219, 15, 73, 64};
    // uint8_t *payload = new uint8_t[4];
    float *angle = (float*) &packets;


    // cout << &payload[0] << ' ' << &payload[1] << endl;
    cout << *angle << endl;

}