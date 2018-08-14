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
        self.cars = [0] * self.members
        self.state = "DELAY"
        self.ready = []

    # calculate the game phase and update it
    def updateGamePhase(self, ID = None):
        # update game state when an "update" message was recieved
        if ID == None and 0 in self.cars:
            return

        # update game state when a "phase" message was recieved
        for i in self.cars:
            if i == 0:
                return
        
        if 0 not in self.cars:
            self.state = "START"
        
        # TODO check to finish game or restart

    # update the car after it posted an update request
    def updateCar(self, ID, data):
        # TODO send back a command
        print("updated car " + str(ID) + "'s coordinates!")
        return "updated"


class Server(BaseHTTPRequestHandler):

    # disable logging and printing every request and response
    def log_request(self, code):
        pass

    def do_GET(self):
        global cars
        global game
        # print all parameters
        print("GET", self.path)
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
            # initiate headers
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # send to game object that the client has sent a new "phase" message
            game.updateGamePhase(path[1])
            
            # send to client the current game's state
            self.wfile.write(bytes(game.state, "utf-8"))
            return

    def do_POST(self):
        global cars
        global game

        print("POST", self.path)
        # split current path for easy processing
        path = self.path.split("/")

        # update all information about the car
        if path[2] == "update":
            data = self.rfile.read(int(self.headers["Content-length"]))

            # calculate response for car
            resp = game.updateCar(path[1], data)

            lock.acquire()
            # update car in game.cars list and update the patch for simulation
            game.cars[int(path[1])] = jsonToCar(data)
            game.cars[int(path[1])].patch = plt.Polygon(calcTriangle(game.cars[int(path[1])].angle, 1 / 20, game.cars[int(path[1])].x,
                                                                     game.cars[int(path[1])].y),
                                                        closed=True, facecolor=["red", "green", "blue"][game.cars[int(path[1])].id])         
            game.cars[int(path[1])].draw()
            # update the game phase
            game.updateGamePhase()
            lock.release()

            # response code for response
            self.send_response(200)
            # add all headers for response
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # write to output file the message content
            self.wfile.write(bytes(resp, "utf-8"))
            return
