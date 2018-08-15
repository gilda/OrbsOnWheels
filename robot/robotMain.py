from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from robotCar import Car, WHEEL_LENGTH, SPIN_TIME
import time

# TODO add the client code for the robot
# TODO make the main function call a thread for networking
#      and a thread for robot timeouts
# TODO check car run time and spin time
# TODO maybe just maybe figure out gyro and positioning feedback
def main():
    # get the motor driver object
    mh = Adafruit_MotorHAT(addr=0x60)

    # create the car
    car1 = Car(mh, 3, 4)

    print("motors are running!")
    print("rotating...")

    while car1.state != car1.stop:
        car1.setVelocity(70)
        car1.move()
        car1.move()

    print("Car stopped!")
    car1.stop()


if __name__ == "__main__":
    main()
