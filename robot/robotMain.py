from robotCar import *
import robotClient
import time
import threading
import atexit

# TODO check car run time and spin time
# TODO maybe just maybe figure out gyro and positioning feedback

USE_MOTOR = True
if USE_MOTOR:
    from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor


def main():
    if USE_MOTOR:
        # get the motor driver object
        mh = Adafruit_MotorHAT(addr=0x60)

    # create the car
    car1 = Car(0, 0.1, mh if USE_MOTOR else None, 3, 4, USE_MOTOR)
    # even if have RunTimeError still stop the motors (e-stop)
    atexit.register(car1.stop)
    car1.setVelocity(50)
    
    print(10 * car1.velocity)
    while car1.state != car1.stop: 
        car1.move_rad(10 * car1.velocity, 90)
        print("angle", car1.angle, ", x", car1.x, ", y", car1.y)

    car1.stop()

    # update thread
    updateThread = threading.Thread(target = robotClient.sendUpdate, args=(car1,))
    # TODO run threads as getting commands from server
    # TODO should always have a command for stopping for e-stop
    for i in range(10):
        if i == 0:
            runThread = threading.Thread(target = car1.rotate, args = (90, ))
            runThread.start()
        else:
             runThread = threading.Thread(target = car1.move)
    robotClient.sendPhase(car1)


if __name__ == "__main__":
    main()
