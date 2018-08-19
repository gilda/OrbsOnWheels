from robotCar import *
import robotClient
import time
import threading

# TODO code Architecture:
#      main calls as a thread the networking infinite loop:
#      the networking infinite loop sends GET and POST commands every n seconds
#      the networking infinite loop parses the command it recieved and calls in a new thread:
#      the thread executes the cars new command to overcome time.sleep() blocking network thread
# TODO check car run time and spin time
# TODO maybe just maybe figure out gyro and positioning feedback

USE_MOTOR = False
if USE_MOTOR:
    from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

def main():
    if USE_MOTOR:
        # get the motor driver object
        mh = Adafruit_MotorHAT(addr=0x60)

    # create the car
    car1 = Car(0, 0.1, mh if USE_MOTOR else None, 3, 4, USE_MOTOR)

    #update thread
    updateThread = threading.Thread(target = robotClient.sendUpdate, args = (car1,))

    robotClient.sendPhase(car1)
    


if __name__ == "__main__":
    main()
