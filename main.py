# libraries
import matplotlib.pyplot as plt
import matplotlib.animation
import math
from car import Car, calcTriangle

# other files
import StateMachine

# window size for plotting
WINDOW_SIZE = 1
# frames per second
FPS = 30


cmd = ""


def iterate(i: int, *fargs):
    # get patches for drawing
    car1 = fargs[0]
    car2 = fargs[1]

    # set new coordiantes for all cars
    car1.setVelocity(0.005)

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
        elif cmd[0] == "RAD":
            car1.move_rad(float(cmd[1]), float(cmd[2]))
    else:
        # continue with current command
        if cmd[0] == "ROTATE":
            car1.rotate(int(cmd[1]))
        elif cmd[0] == "MOVE":
            car1.move_xy(float(cmd[1]), float(cmd[2]))
        elif cmd[0] == "RAD":
            car1.move_rad(float(cmd[1]), float(cmd[2]))
        elif cmd[0] == "DRAW":
            pass

    car1.draw()

    car2.setVelocity(0.005)
    car2.draw()

    # return cars for drawing
    return car1.patch, car2.patch


def main():
    # dooers
    # TODO fix move_rad rotation bugs
    # TODO move_rad fix 0, 360 degrees

    # thinkers
    # TODO make sure velocity is reasonable with WINDOW_SIZE
    # TODO make everything an array of cars (?)

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


# execute code only if file is not imported
if __name__ == "__main__":
    main()
