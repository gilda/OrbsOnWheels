from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from robotCar import Car
import time


def main():
    # get the motor driver object
    mh = Adafruit_MotorHAT(addr=0x60)

    # create the car
    car1 = Car(mh, 3, 4)


if __name__ == "__main__":
    main()
