from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time
import atexit


class Car:
    def __init__(self, mh, rMotor: int, lMotor: int):
        # car's current x position
        self.x: float = 0
        # car's current y position
        self.y: float = 0
        # car's current angle
        self.angle: float = 0

        # car's current velocity
        self.velocity: float = 0

        # car's motors used to control it
        self.rMotor = mh.getMotor(rMotor)
        self.lMotor = mg.getMotor(lMotor)

        # car's state and waiting time
        self.state = None
        self.interval = None

    def stop(self):
        # indicatethat the car has stopped
        self.state = self.stop

        # physically stop the car
        self.rMotor.run(Adafruit_MotorHAT.RELEASE)
        self.lMotor.run(Adafruit_MotorHAT.RELEASE)
