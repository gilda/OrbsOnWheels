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

lock = threading.Lock()

def iterate(i, *fargs):
    # get patches for drawing
    car1 = sv.game.cars[0]
    car2 = sv.game.cars[1]
    car3 = sv.game.cars[2]

    # draw all cars according to their coordinates
    car1.draw()
    car2.draw()
    car3.draw()

    # return cars for drawing
    return car1.patch, car2.patch, car3.patch

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
