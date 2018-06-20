# libraries
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np
import math
import curses

# other files
import StateMachine

# angle in degrees to rad constant
ANGLE_TO_RAD = math.pi / 180
RAD_TO_ANGLE = 180 / math.pi

# window size for plotting
WINDOW_SIZE = 1
# elongation of triangles for ease of seeing degree offset
ELONGATE = 1.2
# frames per second
FPS = 30

# angular velocity of cars
ANGULAR_VELOCITY = 10

cmd = ""

def calcTriangle(angle: int,  size: float, x: float = 0, y: float = 0):
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

def iterate(i: int, *fargs):
    # get patches for drawing
    car1 = fargs[0]
    car2 = fargs[1]

    # set new coordiantes for all cars
    car1.setVelocity(0.01)

    # using global variable to keep track of commands between loops
    global cmd

    # change and ask for new state only if the current state is stop
    # meaning that all current commands were accomplished
    if car1.state == None or car1.state == car1.stop:
        # get new command
        cmd = input("cmd: ")
        cmd = cmd.split(" ")
        if cmd[0] == "ROTATE":
            car1.rotate(int(cmd[1]))
        elif cmd[0] == "MOVE":
            car1.move_xy(float(cmd[1]), float(cmd[2]))
    else:
        # continue with current command
        if cmd[0] == "ROTATE":
            car1.rotate(int(cmd[1]))
        elif cmd[0] == "MOVE":
            car1.move_xy(float(cmd[1]), float(cmd[2]))

    car1.draw()

    car2.setVelocity(0.005)
    car2.draw()

    # return cars for drawing
    return car1.patch, car2.patch


class Car:
    def __init__(self, x: float, y: float, size: float, patch):
        # cars's current coordinates and angle
        self.x: float = x
        self.y: float = y
        self.angle: float = 0

        # car's current size
        self.size: float = size

        # car's velocity in units per second
        self.velocity: float = 0

        # car's patch for drawing ot on plot
        self.patch = patch

        # car's current state
        self.state = self.stop

    # checks if you can change states
    # you change from stop to anything and from anything to stop
    # all changes must pass through a stop
    def stateChange(self, state):
        # if state is the same you can always change to youself or if first iteration
        if self.state == state or self.state == None:
            return True
        # if current state is stop and desired state is not stop
        if self.state == self.stop and state != self.stop:
            return True
        
        # if current state is not stop and desired step is not stop
        if self.state != self.stop and self.state != self.stop:
            return False

    # apply changes for the car's patch for redrawing
    def draw(self):
        self.patch.set_xy(calcTriangle(self.angle, self.size, self.x, self.y))

    # rotate the car
    def rotate(self, angle: float):
        if self.stateChange(self.rotate) != True:
            return
        self.state = self.rotate

        angle = angle % 360
        anglediff = (angle-self.angle+180) % 360 -180

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

    # add to the midpoint
    def move(self):
        if self.stateChange(self.move) != True:
            return
        self.state = self.move

        self.x += self.velocity * math.cos(self.angle * ANGLE_TO_RAD)
        self.y += self.velocity * math.sin(self.angle * ANGLE_TO_RAD)

    # move to specific x, y
    def move_xy(self, x: float, y: float):
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

        #rotate the correct amount to face good directio
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
            elif self.angle == 180 and self.x  - self.velocity < x:
                self.x = x
                self.stop()
                return

        # check over shooting on both axis uf not on straight lines
        if (angle < 90 and overx and overy) or (angle > 90 and angle < 180 and underx and overy) or (angle < 270 and angle > 180 and underx and undery) or (angle < 360 and angle > 270 and overx and undery):
            self.x = x
            self.y = y
            self.stop()
        else:
            self.move()
            self.state = self.move_xy

    # change the current velocity of the car
    def setVelocity(self, v: float):
        self.velocity = v

    # change velocity to zero
    def stop(self):
        self.state = self.stop


def main():
    # TODO fix Car.rotate(angle) when current angle > 180 and angle < 180
    # TODO move with a specific radius and angle
    # TODO make sure velocity is reasonable with WINDOW_SIZE
    # TODO think about making everything an array of cars
    fig = plt.figure()
    ax = plt.axes()
    ax.grid()

    # make axis equal and scaled properly
    ax.axis("equal")
    ax.axis([0, WINDOW_SIZE, 0, WINDOW_SIZE])

    # create car patches for drawing on plot
    car1 = Car(0.5, 0.5, WINDOW_SIZE / 20, plt.Polygon(calcTriangle(0,
                                                                    WINDOW_SIZE / 20), closed=True, facecolor="red"))
    car2 = Car(0.4, 0.4, WINDOW_SIZE / 20, plt.Polygon(calcTriangle(0,
                                                                    WINDOW_SIZE / 20), closed=True, facecolor="blue"))

    # add patches to the drawing
    ax.add_patch(car1.patch)
    ax.add_patch(car2.patch)

    # main animation update function
    anim = matplotlib.animation.FuncAnimation(
        fig, iterate, fargs=[car1, car2], interval=1000 / FPS)
    plt.show()


if __name__ == "__main__":
    main()
