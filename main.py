# libraries
import matplotlib.pyplot as plt
import matplotlib.animation
import math
import threading
import copy

# other files
from Simulation.car import *
import server as sv

# use server
USE_SERVER = True
# window size for plotting
WINDOW_SIZE = 1
# frames per second
FPS = sv.FPS

ax = None

# commands for cars
cmd1 = ""
cmd2 = ""
cmd3 = ""

cmd1Input = ["WAIT 100", "ROT 30", "MOVXY 0.5 0.3", "WAIT 30", "ROT 180"]
cmd1Index = 0

cmd2Input = ["ROT 30", "MOVXY 0.8 0.8", "MOVXY 0.2 0.3", "WAIT 30"]
cmd2Index = 0

cmd3Input = ["RAD 0.2 -90", "MOVXY 0.8 0.6", "WAIT 30", "ROT 180"]
cmd3Index = 0


def iterate(i, *fargs):
    if USE_SERVER:
        global ax

        # clear all of the last patches
        ax.clear()

        # add grid to axis
        ax.grid()
        # make axis equal and scaled properly
        ax.axis("equal")
        ax.axis([0, WINDOW_SIZE, 0, WINDOW_SIZE])

        # add new, updated, patches to draw
        ax.add_patch(sv.game.cars[0].patch)
        ax.add_patch(sv.game.cars[1].patch)
        ax.add_patch(sv.game.cars[2].patch)

        return sv.game.cars[0].patch, sv.game.cars[1].patch, sv.game.cars[2].patch
    else:
        # get patches for drawing
        car1 = fargs[0]
        car2 = fargs[1]
        car3 = fargs[2]
        # set the cars velocity
        car1.setVelocity(0.005)

        # using global variable to keep track of commands between loops
        global cmd1
        global cmd2
        global cmd3

        global cmd1Index
        global cmd1Input
        global cmd2Index
        global cmd2Input
        global cmd3Index
        global cmd3Input

        # change and ask for new state only if the current state is stop
        # meaning that all current commands were accomplished
        if car1.state == None or car1.state == car1.stop:
            # get new command
            #cmd1 = input("cmd1: ")
            if cmd1Index < len(cmd1Input) - 1:
                cmd1 = cmd1Input[cmd1Index]
                cmd1Index += 1
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
            #cmd2 = input("cmd2: ")
            if cmd2Index < len(cmd2Input) - 1:
                cmd2 = cmd2Input[cmd2Index]
                cmd2Index += 1
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

        car2.decInterval()
        car2.draw()

        # set the second cars velocity
        car3.setVelocity(0.005)

        # change and ask for new state only if the current state is stop
        # meaning that ll current commands were accomplished
        if car3.state == None or car3.state == car3.stop:
            # get new command
            #cmd3 = input("cmd3: ")
            if cmd3Index < len(cmd3Input) - 1:
                cmd3 = cmd3Input[cmd3Index]
                cmd3Index += 1
                cmd3 = cmd3.split(" ")
            if cmd3[0] == "ROT":
                car3.rotate(int(cmd3[1]))
            elif cmd3[0] == "MOV":
                car3.move()
            elif cmd3[0] == "MOVXY":
                car3.move_xy(float(cmd3[1]), float(cmd3[2]))
            elif cmd3[0] == "RAD":
                car3.move_rad(float(cmd3[1]), float(cmd3[2]))
            elif cmd3[0] == "WAIT":
                car3.wait(int(cmd3[1]))
            else:
                print("No such command")
        else:
            # continue with current command
            if cmd3[0] == "ROT":
                car3.rotate(int(cmd3[1]))
            elif cmd3[0] == "MOV":
                car3.move()
            elif cmd3[0] == "MOVXY":
                car3.move_xy(float(cmd3[1]), float(cmd3[2]))
            elif cmd3[0] == "RAD":
                car3.move_rad(float(cmd3[1]), float(cmd3[2]))
            elif cmd3[0] == "WAIT":
                car3.decInterval()
            else:
                print("No such command")

        car3.decInterval()
        car3.draw()

        # return cars for drawing
        return car1.patch, car2.patch, car3.patch


def main(cars=[]):
    global ax
    # set up window for drawing
    fig = plt.figure()
    ax = plt.axes()
    ax.grid()

    # make axis equal and scaled properly
    ax.axis("equal")
    ax.axis([0, WINDOW_SIZE, 0, WINDOW_SIZE])

    if USE_SERVER:
        # wait until game has started
        while sv.game.state == "DELAY":
            pass
        print("Game Started!")
    else:
        # create car patches for drawing on plot
        car1 = Car(0, 0.5, 0.5, WINDOW_SIZE / 20, plt.Polygon(calcTriangle(0,
                                                                           WINDOW_SIZE / 20), closed=True, facecolor="red"))
        car2 = Car(1, 0.4, 0.4, WINDOW_SIZE / 20, plt.Polygon(calcTriangle(0,
                                                                           WINDOW_SIZE / 20), closed=True, facecolor="blue"))
        car3 = Car(2, 0.2, 0.6, WINDOW_SIZE / 20, plt.Polygon(calcTriangle(0,
                                                                           WINDOW_SIZE / 20), closed=True, facecolor="green"))
        ax.add_patch(car1.patch)
        ax.add_patch(car2.patch)
        ax.add_patch(car3.patch)

    # main animation update function
    anim = matplotlib.animation.FuncAnimation(
        fig, iterate, fargs=[car1, car2, car3] if not USE_SERVER else None, interval=1000 / FPS)
    plt.show()


# execute code only if file is not imported
if __name__ == "__main__":
    if USE_SERVER:
        # create and run server thread so it will be non-blocking
        serverThread = threading.Thread(target=sv.main)
        serverThread.start()

    # start main and draw animation
    main()
