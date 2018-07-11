from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time
import math

# angle to radians
ANGLE_TO_RAD = math.pi / 180
# radians to angle
RAD_TO_ANGLE = 180 / math.pi

# motor's 100 percent throtle time to revolve around itself once [s]
SPIN_TIME = 0.285
# wheel's one rotation length [cm]
WHEEL_LENGTH = 20
# turning radius [cm]  (car width / 2, because we are using tank drive system)
TURNING_RADIUS = 4.5
# angular velocity of the car [angle/s]
ANGULAR_VELOCITY = 5

class Car:
    def __init__(self, mh, rMotor, lMotor):
        # car's current x position
        self.x = 0
        # car's current y position
        self.y = 0
        # car's current angle
        self.angle = 0

        # car's current velocity
        self.velocity: float = 1

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

        # wait for correct time
        if self.state == self.wait and self.interval == 0:
            return True

        # can always change from stop state
        if self.state == self.stop and state != self.stop:
            return True

        # can always stop whenever needed
        if self.state != self.stop and self.state != self.stop:
            return False

    # car's time to wait with no action
    def wait(self, time):
        self.interval = time
        self.state = self.wait

    # decrease the car's interval by one each iteration
    def decInterval(self):
        if self.interval == 0:
            self.stop()
            self.interval == None
            return
        elif self.interval == None:
            return
        self.interval -= 1

    # update velocity and angle from gyro readings
    def update(self):
        pass
        #self.velocity += getAccelerationForward
        #self.angle = getAngle

    # rotate the car to some desired angle
    def rotate(self, angle):
        if self.stateChange(self.rotate) != True:
            return
        self.state = self.rotate

        # make sure angle is int rangeof full circle
        angle = angle % 360
        # calculate weather to go right or left and how much
        anglediff = (angle-self.angle+180) % 360 + 180

        if self.angle != angle:
            if anglediff > 0:
                # consider overshooting the target angle because ANGULAR_VELOCITY os too high
                if anglediff < ANGULAR_VELOCITY:
                    self.angle = angle
                else:
                    # rotate
                    self.angle = (self.angle + ANGULAR_VELOCITY) % 360
                    
                    # rotate robot
                    self.rMotor.run(Adafruit_MotorHAT.FORWARD)
                    self.lMotor.run(Adafruit_MotorHAT.BACKWARD)
                    time.sleep(SPIN_TIME * (TURNING_RADIUS * math.pi * 2 / WHEEL_LENGTH) * (ANGULAR_VELOCITY / 360))
            else:
                # consider overshhoting target angle
                if anglediff > -ANGULAR_VELOCITY:
                    self.angle = angle
                else:
                    # rotate
                    self.angle = (self.angle - ANGULAR_VELOCITY) % 360

                    # rotate robot
                    self.rMotor.run(Adafruit_MotorHAT.BACKWARD)
                    self.lMotor.run(Adafruit_MotorHAT.FORWARD)
                    time.sleep(SPIN_TIME * (TURNING_RADIUS * math.pi * 2 / WHEEL_LENGTH) * (ANGULAR_VELOCITY / 360))
        else:
            # stop when desired angle was reached
            self.stop()

    # set the car's current velocity
    def setVelocity(self, v):
        self.velocity = v
        self.rMotor.setSpeed(int((v / WHEEL_LENGTH) * 255))
        self.lMotor.setSpeed(int((v / WHEEL_LENGTH) * 255))

    def move(self):
        if self.velocity > 0:    
            # add values to x and y
            self.x += self.velocity * math.cos(self.angle * ANGLE_TO_RAD)
            self.y += self.velocity * math.sin(self.angle * ANGLE_TO_RAD)

            # initiate motors rotation
            self.rMotor.run(Adafruit_MotorHAT.FORWARD)
            self.lMotor.run(Adafruit_MotorHAT.FORWARD)
            
            # wait for correct amount of rotations of the motors
            print((self.velocity / WHEEL_LENGTH) * SPIN_TIME)
            time.sleep((self.velocity / WHEEL_LENGTH)  * SPIN_TIME)
            self.stop()

        elif self.velocity < 0:
            # add values to x and y
            self.x += self.velocity * math.cos(self.angle * ANGLE_TO_RAD)
            self.y += self.velocity * math.sin(self.angle * ANGLE_TO_RAD)

            # initiate motors rotation
            self.rMotor.run(Adafruit_MotorHAT.BACKWARD)
            self.lMotor.run(Adafruit_MotorHAT.BACKWARD)
            
            # wait for correct amount of rotations of the motor
            time.sleep((self.velocity / WHEEL_LENGTH) * SPIN_TIME)
            self.stop()

    # move the car to some desired x y position [cm]
    def move_xy(self, x, y):
        pass
    
    # move the car in some rasius until some angle was achieved
    def move_rad(self, rad, angle):
        pass

    # indicate that the car is now stopping and stop it physically
    def stop(self):
        # indicatethat the car has stopped
        self.state = self.stop

        # physically stop the car
        self.rMotor.run(Adafruit_MotorHAT.RELEASE)
        self.lMotor.run(Adafruit_MotorHAT.RELEASE)

