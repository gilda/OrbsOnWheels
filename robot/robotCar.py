import time
import math
import json

# angle to radians
ANGLE_TO_RAD = math.pi / 180
# radians to angle
RAD_TO_ANGLE = 180 / math.pi

# motor's 100 percent throtle time to revolve around itself once [s]
SPIN_TIME = 0.011
# wheel's one rotation length [cm]
WHEEL_LENGTH = 20
# turning radius [cm]  (car width / 2, because we are using tank drive system)
TURNING_RADIUS = 4.5
# angular velocity of the car [angle/s]
ANGULAR_VELOCITY = 5


def mapFromTo(x, a, b, c, d):
    y = (x-a)/(b-a)*(d-c)+c
    return y


class Car:
    def __init__(self, ID, size, mh, rMotor, lMotor, USE_MOTOR):
        self.id = ID
        self.USE_MOTOR = USE_MOTOR

        # car's current x position
        self.x = 0
        # car's current y position
        self.y = 0
        
        # car's current size
        self.size = size

        # car's current angle
        self.angle = 0

        # car's current velocity
        self.velocity = 1

        if self.USE_MOTOR:
            from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
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

    # TODO implement this
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
            pass
        else:
            # stop when desired angle was reached
            self.stop()

    # TODO implement this
    # set the car's current velocity
    def setVelocity(self, v):
        self.velocity = v
        if self.USE_MOTOR:
            self.rMotor.setSpeed(int(mapFromTo(v, -100, 100, -1, 1) * 255))
            self.lMotor.setSpeed(int(mapFromTo(v, -100, 100, -1, 1) * 255))

    # TODO implement this
    def move(self):
        if self.velocity > 0:
            # add values to x and y
            self.x += self.velocity * math.cos(self.angle * ANGLE_TO_RAD)
            self.y += self.velocity * math.sin(self.angle * ANGLE_TO_RAD)

            if self.USE_MOTOR:
                # initiate motors rotation
                self.rMotor.run(Adafruit_MotorHAT.FORWARD)
                self.lMotor.run(Adafruit_MotorHAT.FORWARD)

            print(WHEEL_LENGTH * SPIN_TIME *
                  mapFromTo(self.velocity, -100, 100, 0, 1))
            # wait for correct amount of rotations of the motors
            time.sleep(WHEEL_LENGTH * SPIN_TIME *
                       mapFromTo(self.velocity, -100, 100, 0, 1))
            self.stop()

        elif self.velocity < 0:
            # add values to x and y
            self.x += self.velocity * math.cos(self.angle * ANGLE_TO_RAD)
            self.y += self.velocity * math.sin(self.angle * ANGLE_TO_RAD)

            if self.USE_MOTOR:
                # initiate motors rotation
                self.rMotor.run(Adafruit_MotorHAT.BACKWARD)
                self.lMotor.run(Adafruit_MotorHAT.BACKWARD)

            # wait for correct amount of rotations of the motor
            time.sleep((self.velocity / WHEEL_LENGTH) * SPIN_TIME)
            self.stop()

    # TODO implement this
    # move the car to some desired x y position [cm]
    def move_xy(self, x, y):
        pass

    # TODO implement this
    # move the car in some rasius until some angle was achieved
    def move_rad(self, rad, angle):
        pass

    # indicate that the car is now stopping and stop it physically
    def stop(self):
        # indicate that the car has stopped
        self.state = self.stop

        if self.USE_MOTOR:
            # physically stop the car
            self.rMotor.run(Adafruit_MotorHAT.RELEASE)
            self.lMotor.run(Adafruit_MotorHAT.RELEASE)

# serialize the cars to json format for sending on the network

def carToJson(car):
    return bytes(json.dumps({"id": car.id,
                             "pos": {"x": car.x,
                                     "y": car.y,
                                     "angle": car.angle},
                             "size": car.size}, indent=4, sort_keys=False), "utf-8")


def jsonToCar(jsonData):
    data = json.loads(jsonData)
    return Car(data["id"], data["pos"]["x"], data["pos"]["y"], data["size"], None, angle = data["pos"]["angle"])

