import math
import json

# angle in degrees to rad constant
ANGLE_TO_RAD = math.pi / 180
RAD_TO_ANGLE = 180 / math.pi
# elongation of triangles for ease of seeing degree offset
ELONGATE = 1.2
# angular velocity of cars
ANGULAR_VELOCITY = 10


def calcTriangle(angle,  size, x=0, y=0):
    # x and y are the center of the triangle
    angle = angle - 90
    point1 = [0, 0]
    point2 = [0, 0]
    point3 = [0, 0]

    # coordinates without rotation aroung center 0,0
    tempPoint1 = [size * math.cos(30 * ANGLE_TO_RAD),  -
                  size * math.sin(30 * ANGLE_TO_RAD) * ELONGATE]
    tempPoint2 = [0, size * ELONGATE]
    tempPoint3 = [-size * math.cos(30 * ANGLE_TO_RAD), -
                  size * math.sin(30 * ANGLE_TO_RAD) * ELONGATE]

    # rotation
    point1[0] = tempPoint1[0] * \
        math.cos(angle * ANGLE_TO_RAD) - \
        tempPoint1[1] * math.sin(angle * ANGLE_TO_RAD)
    point1[1] = tempPoint1[0] * \
        math.sin(angle * ANGLE_TO_RAD) + \
        tempPoint1[1] * math.cos(angle * ANGLE_TO_RAD)

    point2[0] = tempPoint2[0] * \
        math.cos(angle * ANGLE_TO_RAD) - \
        tempPoint2[1] * math.sin(angle * ANGLE_TO_RAD)
    point2[1] = tempPoint2[0] * \
        math.sin(angle * ANGLE_TO_RAD) + \
        tempPoint2[1] * math.cos(angle * ANGLE_TO_RAD)

    point3[0] = tempPoint3[0] * \
        math.cos(angle * ANGLE_TO_RAD) - \
        tempPoint3[1] * math.sin(angle * ANGLE_TO_RAD)
    point3[1] = tempPoint3[0] * \
        math.sin(angle * ANGLE_TO_RAD) + \
        tempPoint3[1] * math.cos(angle * ANGLE_TO_RAD)

    # shift into x,y poistion
    point1[0] += x
    point1[1] += y

    point2[0] += x
    point2[1] += y

    point3[0] += x
    point3[1] += y

    # return points for drawing
    return [point1, point2, point3]


class Car:
    def __init__(self, ID, x, y, size, patch, angle=0):
        self.id = ID

        # cars's current coordinates and angle
        self.x = x
        self.y = y
        self.angle = angle

        # car's current size
        self.size = size

        # car's velocity in units per second
        self.velocity = 0

        # car's patch for drawing ot on plot
        self.patch = patch

        # car's current state
        self.state = None

        # car's waiting time
        self.interval = None

    # checks if you can change states
    # you change from stop to anything and from anything to stop
    # all changes must pass through a stop
    def stateChange(self, state):
        # if state is the same you can always change to youself or if first iteration
        if self.state == state or self.state == None:
            return True

        # wait for correct time
        if self.state == self.wait and self.interval == 0:
            return True

        # if current state is stop and desired state is not stop
        if self.state == self.stop and state != self.stop:
            return True

        # if current state is not stop and desired step is not stop
        if self.state != self.stop and self.state != self.stop:
            return False

    # cars time to wait with no action
    def wait(self, time):
        self.interval = time
        self.state = self.wait

    # decrease the cars interval by one each frame
    def decInterval(self):
        if self.interval == 0:
            self.stop()
            self.interval = None
            return
        elif self.interval == None:
            return
        self.interval -= 1

    # apply changes for the car's patch for redrawing
    def draw(self):
        self.patch.set_xy(calcTriangle(self.angle, self.size, self.x, self.y))

    # rotate the car
    def rotate(self, angle):
        if self.stateChange(self.rotate) != True:
            return
        self.state = self.rotate

        angle = angle % 360
        anglediff = (angle-self.angle+180) % 360 - 180

        # add or subtract angle if desired angle wasnt reached yet
        if self.angle != angle:
            if anglediff > 0:
                if anglediff < ANGULAR_VELOCITY:
                    self.angle = angle
                else:
                    self.angle = (self.angle + ANGULAR_VELOCITY) % 360
            else:
                if anglediff > -ANGULAR_VELOCITY:
                    self.angle = angle
                else:
                    self.angle = (self.angle - ANGULAR_VELOCITY) % 360
        else:
            self.stop()

    # add to the midpoint the sin and cos for x and y values
    def move(self):
        if self.stateChange(self.move) != True:
            return
        self.state = self.move

        self.x += self.velocity * math.cos(self.angle * ANGLE_TO_RAD)
        self.y += self.velocity * math.sin(self.angle * ANGLE_TO_RAD)

        self.stop()

    # move to specific x, y
    def move_xy(self, x, y):
        # state cannot change
        if self.stateChange(self.move_xy) != True:
            return

        # reached target
        if self.x == x and self.y == y:
            self.stop()
            return

        # check for straight lines of driving along the axes
        if (self.x-x == 0 or self.y-y == 0) and self.x > x:
            angle = 180
        elif (self.x-x == 0 or self.y-y == 0) and self.x < x:
            angle = 0
        elif (self.x-x == 0 or self.y-y == 0) and self.y > y:
            angle = 270
        elif (self.x-x == 0 or self.y-y == 0) and self.y < y:
            angle = 90
        else:
            # calculate angle you should drive to get there the fastest
            angle = math.atan((y-self.y)/(x-self.x)) * RAD_TO_ANGLE
            if self.x > x:
                # if angle should be 90<angle<270
                angle = (angle-180) % 360

        # rotate the correct amount to face good directio
        self.stop()
        self.rotate(angle)

        # check if you can overshoot due to high velocity
        overx = (self.x + self.velocity *
                 math.cos(self.angle * ANGLE_TO_RAD)) > x
        underx = (self.x + self.velocity *
                  math.cos(self.angle * ANGLE_TO_RAD)) < x
        overy = (self.y + self.velocity *
                 math.sin(self.angle * ANGLE_TO_RAD)) > y
        undery = (self.y + self.velocity *
                  math.sin(self.angle * ANGLE_TO_RAD)) < y

        # check overshooting on straight lines on the y axis
        if self.x == x and (self.angle == 90 or self.angle == 270):
            if self.angle == 90 and self.y + self.velocity > y:
                self.y = y
                self.stop()
                return
            elif self.angle == 270 and self.y - self.velocity < y:
                self.y = y
                self.stop()
                return

        # check overshooting on straight lines on the y axis
        if self.y == y and (self.angle == 0 or self.angle == 180):
            if self.angle == 0 and self.x + self.velocity > x:
                self.x = x
                self.stop()
                return
            elif self.angle == 180 and self.x - self.velocity < x:
                self.x = x
                self.stop()
                return

        # check over shooting on both axis if not on straight lines
        if (angle < 90 and overx and overy) or (angle > 90 and angle < 180 and underx and overy) or (angle < 270 and angle > 180 and underx and undery) or (angle < 360 and angle > 270 and overx and undery):
            self.x = x
            self.y = y
            self.stop()
        else:
            self.move()
            self.state = self.move_xy

    # move the car in radius for a specified angle
    def move_rad(self, rad, angle):
        if not self.stateChange(self.move_rad):
            return
        self.state = self.move_rad

        # avoid division by zero
        angle = 360 if angle == 0 else angle
        anglediff = (angle-self.angle+180) % 360 - 180

        if anglediff == 0:
            # finished
            self.stop()
            return

        # remember last velocity
        pVelocity = self.velocity

        # number of iterations to complete an arch
        numIterAngle = angle / ANGULAR_VELOCITY
        # velocity needed to complete all the distance according to maximum angular velocity
        numIterMove = (rad * angle * ANGLE_TO_RAD) / numIterAngle

        # make sure the velocity of the car doesnt excees its maximum
        if pVelocity < numIterMove:
            # number of iteratrions for the maximum value of velicity
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
            # jump to angle if needed and check overshooting
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

        anglediff = (angle-self.angle+180) % 360 - 180

        # return if desired angle was reached
        if anglediff == 0:
            # finished
            self.stop()
            return
        else:
            # not finished
            self.state = self.move_rad
            return

    # change the current velocity of the car
    def setVelocity(self, v):
        self.velocity = v

    # change state to stop so next command can be interpreted
    def stop(self):
        self.state = self.stop

# serialize the cars to json format for sending on the network


def carToJson(car):
    return bytes(json.dumps({"id": car.id,
                             "pos": {"x": car.x,
                                     "y": car.y,
                                     "angle": car.angle},
                             "size": car.size}, indent=4, sort_keys=False), "utf-8")


def jsonToCar(jsonData):
    data = json.loads(jsonData)
    return Car(data["id"], data["pos"]["x"], data["pos"]["y"], data["size"], None, angle=data["pos"]["angle"])
