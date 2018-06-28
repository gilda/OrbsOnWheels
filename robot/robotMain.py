from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from robotCar import Car
import time


def main():
    # get the motor driver object
    mh = Adafruit_MotorHAT(addr=0x60)

    # create the car
    car1 = Car(mh, 4, 3)

    print("motors are running!")
    car1.setVelocity(255)
    car1.move()
    print("Car stopped!")
    car1.stop()

if __name__ == "__main__":
    main()
