from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from robotCar import Car, WHEEL_LENGTH, SPIN_TIME
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
