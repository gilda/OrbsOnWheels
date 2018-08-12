# libraries
import matplotlib.pyplot as plt
import matplotlib.animation
import math
import threading

# other files
from Simulation.car import *
import server as sv

# window size for plotting
WINDOW_SIZE = 1
# frames per second
FPS = 20

def iterate(i, *fargs):
    # get patches for drawing
    car1 = fargs[0]
    car2 = fargs[1]
    car3 = fargs[2]

    # set the cars velocity
    car1.setVelocity(0.005)

    # change and ask for new state only if the current state is stop
    # meaning that all current commands were accomplished
    if car1.state == None or car1.state == car1.stop:
        # get new command
        # TODO get command from server to show that cars are moving!
        cmd1 = input("cmd1: ")
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
        # TODO get command from server to show that cars are moving!
        cmd2 = input("cmd2: ")
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
        # TODO get command from server to show that cars are moving!
        cmd3 = input("cmd3: ")
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
    fig = plt.figure()
    ax = plt.axes()
    ax.grid()

    # make axis equal and scaled properly
    ax.axis("equal")
    ax.axis([0, WINDOW_SIZE, 0, WINDOW_SIZE])

    while sv.game.state == "DELAY":
        pass

    print("Game Started!")

    for i in sv.game.cars:
        i.patch = plt.Polygon(calcTriangle(0, WINDOW_SIZE / 20, i.x, i.y), closed=True, facecolor=["red","green","blue"][i.id])
        ax.add_patch(i.patch)

    # main animation update function
    anim = matplotlib.animation.FuncAnimation(
        fig, iterate, fargs=sv.game.cars, interval=1000 / FPS)
    plt.show()


# execute code only if file is not imported
if __name__ == "__main__":
    serverThread = threading.Thread(target = sv.main)
    serverThread.start()
    main()
