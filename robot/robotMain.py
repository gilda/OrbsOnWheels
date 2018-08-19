from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from robotCar import *
from robotClient import *
import time

# TODO code Architecture:
#      main calls two functions from the networking:
#      1: poll for command and execute. (should be non-blocking) threading.Thread(target = func, args = (func args tuple)).start()
#      2: send update. (could block maybe? sent on an interval of X milliseconds) https://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds
#      networking updates the server about the where-abouts of the car
#      the main function parses any command that the car recieved.
#      the robotCar executes the command given and updates the cars position parameters for the networking.
#      import main <- robotClient
#               ^  <- robotCar
#
# TODO check car run time and spin time
# TODO maybe just maybe figure out gyro and positioning feedback

def main():
    # get the motor driver object
    mh = Adafruit_MotorHAT(addr=0x60)

    # create the car
    car1 = Car(0, 0.1, mh, 3, 4)

    #update thread
    updateThread = threading.Thread(target = robotClient.sendUpdate, args = (car1))

    sendPhase(car1)
    time.sleep(5)
    while True:
        x = updateThread.start()
        print(x)
        updateThread.join()


if __name__ == "__main__":
    main()
