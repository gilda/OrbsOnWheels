# libraries
import matplotlib.pyplot as plt
import matplotlib.animation
import math
import threading
import copy

# other files
from Simulation.car import *
import server as sv

# window size for plotting
WINDOW_SIZE = 1
# frames per second
FPS = 20

ax = None


def iterate(i, *fargs):
    return [sv.game.cars[0].patch, sv.game.cars[1].patch, sv.game.cars[2].patch]


def main(cars=[]):
    global ax
    # set up window for drawing
    fig = plt.figure()
    ax = plt.axes()
    ax.grid()

    # make axis equal and scaled properly
    ax.axis("equal")
    ax.axis([0, WINDOW_SIZE, 0, WINDOW_SIZE])

    # wait until game has started
    while sv.game.state == "DELAY":
        pass
    print("Game Started!")

    # main animation update function
    anim = matplotlib.animation.FuncAnimation(
        fig, iterate, interval=1000 / FPS)
    plt.show()


# execute code only if file is not imported
if __name__ == "__main__":
    # create and run server thread so it will be non-blocking
    serverThread = threading.Thread(target=sv.main)
    serverThread.start()

    # start main and draw animation
    main()
