#include <iostream>

using namespace std;

int main() {
    enum WheelDirection {forward = 1, backward = 0};
    WheelDirection left_motor_direction = forward;
    WheelDirection right_motor_direction = backward;

    if (left_motor_direction == forward) {
        cout << "Forward" << endl;
    }
    if (right_motor_direction == backward) {
        cout << "backward" << endl;
    }


    return 0;

}