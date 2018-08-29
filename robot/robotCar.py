import time
import math
import json
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor


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
ANGULAR_VELOCITY = 10


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

    # rotate the car to some desired angle
    def rotate(self, angle):
        if self.stateChange(self.rotate) != True:
            return
        self.state = self.rotate

        # make sure angle is int rangeof full circle
        angle = angle % 360
        # calculate weather to go right or left and how much
        anglediff = (angle-self.angle+180) % 360 - 180

        if self.angle != angle:
            if anglediff > 0:
                # make sure not to overshoot
                if anglediff < ANGULAR_VELOCITY:
                    self.angle = angle
                    self.stop()
                else:
                    # change angle of car
                    self.angle = (self.angle + ANGULAR_VELOCITY) % 360

                    # only if using the motors of the rpi
                    if self.USE_MOTOR:
                        # run motors
                        self.rMotor.run(Adafruit_MotorHAT.FORWARD)
                        self.lMotor.run(Adafruit_MotorHAT.BACKWARD)
                        time.sleep(ANGULAR_VELOCITY * SPIN_TIME)
            else:
                # make sure not to overshoot
                if anglediff > -ANGULAR_VELOCITY:
                    self.angle = angle
                    self.stop()
                else:
                    # change the angle of the car
                    self.angle = (self.angle - ANGULAR_VELOCITY) % 360

                    if self.USE_MOTOR:
                        # run motors
                        self.rMotor.run(Adafruit_MotorHAT.BACKWARD)
                        self.lMotor.run(Adafruit_MotorHAT.FORWARD)
                        time.sleep(ANGULAR_VELOCITY * SPIN_TIME)
        else:
            # stop when desired angle was reached
            self.stop()

    # set the car's current velocity
    def setVelocity(self, v):
        self.velocity = v
        if self.USE_MOTOR:
            v = abs(v)
            self.rMotor.setSpeed(int(mapFromTo(v, 0, 100, 0, 255)))
            self.lMotor.setSpeed(int(mapFromTo(v, 0, 100, 0, 255)))

    # move the car one velocity unit
    def move(self):
        if self.stateChange(self.move) != True:
            return
        self.state = self.move

        if self.velocity > 0:
            # add values to x and y
            self.x += self.velocity * math.cos(self.angle * ANGLE_TO_RAD)
            self.y += self.velocity * math.sin(self.angle * ANGLE_TO_RAD)

            if self.USE_MOTOR:
                # initiate motors rotation
                self.rMotor.run(Adafruit_MotorHAT.FORWARD)
                self.lMotor.run(Adafruit_MotorHAT.FORWARD)

            # wait for correct amount of rotations of the motors
            time.sleep(WHEEL_LENGTH * SPIN_TIME)
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
            time.sleep(WHEEL_LENGTH * SPIN_TIME)
            self.stop()

    # move the car to some desired x and y position
    def move_xy(self, x, y):
        # state cannot change
        if self.stateChange(self.move_xy) != True:
            return

        # reached target
        if self.x == x and self.y == y:
            self.stop()
            return

        # check for straight lines of driving along the axes
        if (self.x - x == 0 or self.y - y == 0) and self.x > x:
            angle = 180
        elif (self.x - x == 0 or self.y - y == 0) and self.x < x:
            angle = 0
        elif (self.x - x == 0 or self.y - y == 0) and self.y > y:
            angle = 270
        elif (self.x - x == 0 or self.y - y == 0) and self.y < y:
            angle = 90
        else:
            # calculate angle you should drive to get there the fastest
            angle = math.atan((y - self.y) / (x - self.x)) * RAD_TO_ANGLE
            if self.x > x:
                # if angle should be 90 < angle < 270
                angle = (angle - 180) % 360

        angle = angle % 360
        # rotate the correct amount to  face the roght direction
        self.stop()
        self.rotate(angle)

        # check overshhoting
        overx = (self.x + self.velocity *
                 math.cos(self.angle * ANGLE_TO_RAD)) > x
        underx = (self.x + self.velocity *
                  math.cos(self.angle * ANGLE_TO_RAD)) < x
        overy = (self.y + self.velocity *
                 math.sin(self.angle * ANGLE_TO_RAD)) > y
        undery = (self.y + self.velocity *
                  math.sin(self.angle * ANGLE_TO_RAD)) < y

        # check for overshooting due to high velocity
        if self.x == x and (self.angle == 90 or self.angle == 270):
            if self.angle == 90 and self.y + self.velocity > y:
                self.y = y
                self.stop()
                return
            elif self.angle == 270 and self.y - self.velocity < y:
                self.y = y
                self.stop()
                return

        # check for overshooting on straight lines on the x axis
        if self.y == y and (self.angle == 0 or self.angle == 180):
            if self.angle == 0 and self.x + self.velocity > x:
                self.x = x
                self.stop()
                return
            elif self.angle == 180 and self.x - self.velocity < x:
                self.x = x
                self.stop()
                return

        # check overshooting on both axes if not on straight line
        if (angle < 90 and overx and overy) or (angle > 90 and angle < 180 and underx and overy) or (angle < 270 and angle > 180 and underx and undery) or (angle < 360 and angle > 270 and overx and undery):
            self.x = x
            self.y = y
            self.stop()
        else:
            self.move()
            self.state = self.move_xy

    # TODO implement this with a set of points and mov_xy? not sure but this way less noise
    # move the car in some rasius until some angle was achieved
    def move_rad(self, rad, angle):
        # state cannnot change
        if not self.stateChange(self.move_rad):
            return
        self.state = self.move_rad

        # avoid division by zero
        angle = 360 if angle == 0 else angle
        anglediff = (angle - self.angle+180) % 360 - 180

        # finished rotating
        if anglediff == 0:
            self.stop()
            return

        # remember last velocity
        pVelocity = self.velocity

        # number of iterations to complete an arch
        numIterAngle = angle / ANGULAR_VELOCITY
        # velocity needed to complete all the distance according to maximum angular velocity
        numIterMove = (rad * angle * ANGLE_TO_RAD) / numIterAngle

        # make sure the velociry of the car doesn't exceed it's limit
        if pVelocity < numIterMove:
            # number of iterations for the maximum value of velocity
            numIterMove = (rad * angle * ANGLE_TO_RAD) / pVelocity
            # number of angles to turn to complete an arch
            numIterAngle = angle / numIterMove

        self.state = self.stop
        # choose direction to rotate
        if anglediff >= 0:
            # jump to angle if needed and check overshooting
            if anglediff < numIterAngle:
                self.angle = angle
            else:
                self.rotate(self.angle + numIterAngle)
        else:
            if abs(anglediff) < numIterAngle:
                self.angle = angle % 360
            else:
                self.rotate(self.angle - numIterAngle)

        self.state = self.stop
        # move according to velocity
        self.setVelocity(pVelocity if numIterMove == (
            rad * angle * ANGLE_TO_RAD) / pVelocity else numIterMove)
        self.move()
        # reset back velocity to previous one
        self.setVelocity(pVelocity)

        anglediff = (angle - self.angle) % 360 - 180

        # return if desired angle was reached
        if anglediff == 0:
            # finished
            self.stop()
        else:
            # not finished
            self.state = self.move_rad
            return

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
                             "state": "None" if car.state == None else
                                      "stop" if car.state == car.stop else
                                      "wait" if car.state == car.wait else
                                      "rotate" if car.state == car.rotate else
                                      "move" if car.state == car.move else
                                      "move_xy" if car.state == car.move_xy else
                                      "move_rad" if car.state == car.move_rad else None,
                             "pos": {"x": car.x,
                                     "y": car.y,
                                     "angle": car.angle},
                             "size": car.size}, indent=4, sort_keys=False), "utf-8")


def jsonToCar(jsonData):
    data = json.loads(jsonData)
    c = Car(data["id"], data["pos"]["x"], data["pos"]["y"],
            data["size"], None, angle=data["pos"]["angle"])
    if data["state"] == "None":
        c.state = None
    elif data["state"] = "stop":
        c.state = c.stop
    elif data["state"] == "wait":
        c.state = c.wait
    elif data["state"] == "rotate":
        c.state = c.rotate
    elif data["state"] == "move":
        c.state = c.move
    elif data["state"] == "move_xy":
        c.state = c.move_xy
    elif data["state"] == "move_rad":
        c.state = c.move_rad
    return c
