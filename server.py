from http.server import *
from Simulation.car import *
import time
import matplotlib.pyplot as plt
import threading

# initiate this module's game object
game = None
lock = threading.Lock()


def main():
    # construct game
    global game
    game = Game(3, [])

    # start http server and serve
    httpd = HTTPServer(("127.0.0.1", 4590), Server)
    httpd.serve_forever()


class Game:
    def __init__(self, members, cars):
        # game always starts with DELAY
        self.members = members
        self.cars = [None] * self.members
        self.state = "DELAY"
        self.ready = []

    # calculate the game phase and update it
    def updateGamePhase(self, ID):
        # once all cars have stated that they are ready the game will start
        if self.members == len(self.ready):
            # make sure all cars have sent their coordinates
            for i in self.cars:
                if i == None:
                    return

            self.state = "START"
            return
        # TODO check to finish game or restart

    # update the car after it posted an update request
    def updateCar(self, ID, data):
        # TODO send a command
        print("updated")
        return "updated"


class Server(BaseHTTPRequestHandler):

    # disable logging and printing every request and response
    def log_request(self, code):
        pass

    def do_GET(self):
        global cars
        global game
        # print all parameters
        print(self.path)
        # print(self.headers)

        # print all cars in json format
        if self.path == "/":
            # initiate headers
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # send json of all cars
            for car in cars:
                self.wfile.write(carToJson(car)+"\r\n")
            return

        # split path to for easy porcessing
        path = self.path.split("/")

        # the car is asking for the current phase
        if path[2] == "phase":
            # list all cars that are ready to start the game
            if not path[1] in game.ready and game.state == "DELAY":
                game.ready.append(path[1])

            # initiate headers
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # send current state of all the cars
            game.updateGamePhase(path[2])
            self.wfile.write(bytes(game.state, "utf-8"))
            return

    def do_POST(self):
        global cars
        global game

        # split current path for easy processing
        path = self.path.split("/")

        # update all information about the car
        if path[2] == "update":
            data = self.rfile.read(int(self.headers["Content-length"]))

            # calculate response for car
            resp = game.updateCar(path[1], data)

            #lock.acquire(blocking = True)
            # update car in game.cars list
            game.cars[int(path[1])] = jsonToCar(data)
            game.cars[int(path[1])].patch = plt.Polygon(calcTriangle(game.cars[int(path[1])].angle, 1 / 20, game.cars[int(path[1])].x,
                                                                     game.cars[int(path[1])].y),
                                                        closed=True, facecolor=["red", "green", "blue"][game.cars[int(path[1])].id])
            game.cars[int(path[1])].draw()
            # lock.release()

            # response code for response
            self.send_response(200)
            # add all headers for response
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # write to output file the message content
            self.wfile.write(bytes(resp, "utf-8"))
            return
