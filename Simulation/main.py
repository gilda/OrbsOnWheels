# libraries
import matplotlib.pyplot as plt
import matplotlib.animation
import math

# other files
from car import *


# window size for plotting
WINDOW_SIZE = 1
# frames per second
FPS = 30

# commands for cars
cmd1 = ""
cmd2 = ""


def iterate(i, *fargs):
    # get patches for drawing
    car1 = fargs[0]
    car2 = fargs[1]

    # set the cars velocity
    car1.setVelocity(0.005)

    # using global variable to keep track of commands between loops
    global cmd1
    global cmd2

    # change and ask for new state only if the current state is stop
    # meaning that all current commands were accomplished
    if car1.state == None or car1.state == car1.stop:
        # get new command
        cmd1 = input("cmd1: ")
        cmd1 = cmd1.split(" ")
        if cmd1[0] == "ROT":
            car1.rotate(int(cmd1[1]))
        elif cmd1[0] == "MOV":
            car1.move()
        elif cmd1[0] == "MOVXY":
            car1.move_xy(float(cmd1[1]), float(cmd1[2]))
        elif cmd1[0] == "RAD":
            car1.move_rad(float(cmd1[1]), float(cmd1[2]))
        elif cmd1[0] == "WAIT":
            car1.wait(int(cmd1[1]))
        else:
            print("No such command")
    else:
        # continue with current command
        if cmd1[0] == "ROT":
            car1.rotate(int(cmd1[1]))
        elif cmd1[0] == "MOV":
            car1.move()
        elif cmd1[0] == "MOVXY":
            car1.move_xy(float(cmd1[1]), float(cmd1[2]))
        elif cmd1[0] == "RAD":
            car1.move_rad(float(cmd1[1]), float(cmd1[2]))
        elif cmd1[0] == "WAIT":
            car1.decInterval()
        else:
            print("No such command")

    # draw the car after all changes were made
    car1.decInterval()
    car1.draw()

    # set the second cars velocity
    car2.setVelocity(0.005)

    # change and ask for new state only if the current state is stop
    # meaning that ll current commands were accomplished
    if car2.state == None or car2.state == car2.stop:
        # get new command
        cmd2 = input("cmd2: ")
        cmd2 = cmd2.split(" ")
        if cmd2[0] == "ROT":
            car2.rotate(int(cmd2[1]))
        elif cmd2[0] == "MOV":
            car2.move()
        elif cmd2[0] == "MOVXY":
            car2.move_xy(float(cmd2[1]), float(cmd2[2]))
        elif cmd2[0] == "RAD":
            car2.move_rad(float(cmd2[1]), float(cmd2[2]))
        elif cmd2[0] == "WAIT":
            car2.wait(int(cmd2[1]))
        else:
            print("No such command")
    else:
        # continue with current command
        if cmd2[0] == "ROT":
            car2.rotate(int(cmd2[1]))
        elif cmd2[0] == "MOV":
            car2.move()
        elif cmd2[0] == "MOVXY":
            car2.move_xy(float(cmd2[1]), float(cmd2[2]))
        elif cmd2[0] == "RAD":
            car2.move_rad(float(cmd2[1]), float(cmd2[2]))
        elif cmd2[0] == "WAIT":
            car2.decInterval()
        else:
            print("No such command")

    car2.draw()

    # return cars for drawing
    return car1.patch, car2.patch


def main():
    # dooers
    # TODO fix waiting and stopping of all commands

    # thinkers
    # TODO make sure velocity is reasonable within WINDOW_SIZE
    # TODO make everything an array of cars (?)

    fig = plt.figure()
    ax = plt.axes()
    ax.grid()

    # make axis equal and scaled properly
    ax.axis("equal")
    ax.axis([0, WINDOW_SIZE, 0, WINDOW_SIZE])

    # create car patches for drawing on plot
    car1 = Car(0, 0.5, 0.5, WINDOW_SIZE / 20, plt.Polygon(calcTriangle(0,
                                                                    WINDOW_SIZE / 20), closed=True, facecolor="red"))
    car2 = Car(1, 0.4, 0.4, WINDOW_SIZE / 20, plt.Polygon(calcTriangle(0,
                                                                    WINDOW_SIZE / 20), closed=True, facecolor="blue"))

    # add patches to the drawing
    ax.add_patch(car1.patch)
    ax.add_patch(car2.patch)

    # main animation update function
    anim = matplotlib.animation.FuncAnimation(
        fig, iterate, fargs=[car1, car2], interval=1000 / FPS)
    plt.show()


# execute code only if file is not imported
if __name__ == "__main__":
    main()
