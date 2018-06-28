from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time
import atexit

# motor's 100 percent throtle time to revolve around itself once
SPIN_TIME = 0.285

# wheel's one rotation length

# car's maximum velocity

class Car:
    def __init__(self, mh, rMotor, lMotor):
        # car's current x position
        self.x = 0
        # car's current y position
        self.y = 0
        # car's current angle
        self.angle = 0

        # car's current velocity
        self.velocity = 0

        # car's motors used to control it
        self.rMotor = mh.getMotor(rMotor)
        self.lMotor = mh.getMotor(lMotor)

        # car's state and waiting time
        self.state = None
        self.interval = None
    
    def stateChange(self, state):
        # can always change to current state
        if self.state == state or self.state == None:
            return True

        # can always change from stop state
        if self.state == self.stop and state != self.stop:
            return True

        # can always stop whenever needed
        if self.state != self.stop and self.state != self.stop:
            return False

    def setVelocity(self, v):
        self.velocity = v
        self.rMotor.setSpeed(v)
        self.lMotor.setSpeed(v)

    def move(self):
        if self.velocity > 0:
            # initiate motors rotation
            self.rMotor.run(Adafruit_MotorHAT.FORWARD)
            self.lMotor.run(Adafruit_MotorHAT.FORWARD)
            # wait for correct amount of rotations of the motors
            time.sleep(SPIN_TIME / (self.velocity / 255))
        elif self.velocity < 0:
            # initiate motors rotation
            self.rMotor.run(Adafruit_MotorHAT.BACKWARD)
            self.lMotor.run(Adafruit_MotorHAT.BACKWARD)
            # wait for correct amount of rotations of the motor
            time.sleep(SPIN_TIME / (self.velocity / 255))

    def stop(self):
        # indicatethat the car has stopped
        self.state = self.stop

        # physically stop the car
        self.rMotor.run(Adafruit_MotorHAT.RELEASE)
        self.lMotor.run(Adafruit_MotorHAT.RELEASE)
