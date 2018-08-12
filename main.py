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
    try:
        sv.lock.release()
    except:
        pass
    sv.lock.acquire()
    return sv.game.cars[0].patch, sv.game.cars[0].patch, sv.game.cars[0].patch

def main(cars=[]):
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

    # create an intial polygon for all cars
    for i in sv.game.cars:
        i.patch = plt.Polygon(calcTriangle(0, 1 / 20, i.x, i.y), closed=True, facecolor=["red","green","blue"][i.id])
        ax.add_patch(i.patch)

    # main animation update function
    anim = matplotlib.animation.FuncAnimation(
        fig, iterate, interval=1000 / FPS)
    plt.show()


# execute code only if file is not imported
if __name__ == "__main__":
    # create and run server thread so it will be non-blocking
    serverThread = threading.Thread(target = sv.main)
    serverThread.start()
    
    # start main and draw animation
    main()
