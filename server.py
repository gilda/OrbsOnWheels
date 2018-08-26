from http.server import *
from Simulation.car import *
import time
import matplotlib.pyplot as plt
import threading

HOST = "127.0.0.1"
PORT = 4590

# initiate this module's game object
game = None
lock = threading.Lock()
FPS = 10

SEND_COMMAND = False

cmd0 = ""
cmd1 = ""
cmd2 = ""

cmd0Input = ["ROT 30", "MOVXY 0.8 0.8", "MOVXY 0.2 0.3", "WAIT 30"]
cmd0Index = 0

cmd1Input = ["WAIT 100", "ROT 30", "MOVXY 0.5 0.3", "WAIT 30", "ROT 180"]
cmd1Index = 0

cmd2Input = ["RAD 0.2 -90", "MOVXY 0.8 0.6", "WAIT 30", "ROT 180"]
cmd2Index = 0


def main():
    # construct game
    global game
    game = Game(3, [])

    # start http server and serve
    httpd = HTTPServer((HOST, PORT), Server)
    httpd.serve_forever()


class Game:
    def __init__(self, members, cars):
        # game always starts with DELAY
        self.members = members
        self.cars = [0] * self.members
        self.state = "DELAY"
        self.ready = []

    # calculate the game phase and update it
    def updateGamePhase(self, ID=None):
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
        # wether using ORBS or not

    # update the car after it posted an update request
    def updateCar(self, ID, data, USE_NET = False):
        #print("updated car " + str(ID) + "'s coordinates!")        
        if USE_NET:
            # TODO send car's data and get back a command using ORBS
            pass
        else:
            # use pre defined commands to run
            global cmd0
            global cmd1
            global cmd2

            global cmd0Index
            global cmd0Input
            global cmd1Index
            global cmd1Input
            global cmd2Index
            global cmd2Input

            if ID == 0:
                if self.getCarById(ID).state == None or self.getCarById(ID).state == self.getCarById(ID).stop or self.getCarById(ID).interval == 0:
                    if cmd0Index < len(cmd0Input) - 1:
                        cmd0 = cmd0Input[cmd0Index]
                        cmd0Index += 1
                    return cmd0
                else:
                    return cmd0
            
            if ID == 1:
                if self.getCarById(ID).state == None or self.getCarById(ID).state == self.getCarById(ID).stop or self.getCarById(ID).interval == 0:
                    if cmd1Index < len(cmd1Input) - 1:
                        cmd1 = cmd1Input[cmd1Index]
                        cmd1Index += 1
                    return cmd1
                else:
                    return cmd1

            if ID == 2:
                if self.getCarById(ID).state == None or self.getCarById(ID).state == self.getCarById(ID).stop or self.getCarById(ID).interval == 0:
                    if cmd2Index < len(cmd2Input) - 1:
                        cmd2 = cmd2Input[cmd2Index]
                        cmd2Index += 1
                    return cmd2
                else:
                    return cmd2
            return ""

    # return the car with the specified ID
    def getCarById(self, ID):
        for c in game.cars:
            if c.id == ID:
                return c
        return None


class Server(BaseHTTPRequestHandler):

    # disable logging and printing every request and response
    def log_request(self, code):
        pass

    def do_GET(self):
        global cars
        global game
        # print all parameters
        #print("GET", self.path)

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

        #print("POST", self.path)
        # split current path for easy processing
        path = self.path.split("/")

        # update all information about the car
        if path[2] == "update":
            data = self.rfile.read(int(self.headers["Content-length"]))
            lock.acquire()
            
            # update car in game.cars list and update the patch for simulation
            game.cars[int(path[1])] = jsonToCar(data)
            game.cars[int(path[1])].patch = plt.Polygon(calcTriangle(game.cars[int(path[1])].angle, 1 / 20, game.cars[int(path[1])].x,
                                                                     game.cars[int(path[1])].y),
                                                        closed=True, facecolor=["red", "green", "blue"][game.cars[int(path[1])].id])         
            
            game.cars[int(path[1])].draw()
            if game.cars[int(path[1])] != 0 and SEND_COMMAND:
                resp = game.updateCar(int(path[1]), data)
            else:
                game.cars[int(path[1])] = jsonToCar(data)
                game.cars[int(path[1])].patch = plt.Polygon(calcTriangle(game.cars[int(path[1])].angle, 1 / 20, game.cars[int(path[1])].x,
                                                                     game.cars[int(path[1])].y),
                                                        closed=True, facecolor=["red", "green", "blue"][game.cars[int(path[1])].id])
                game.cars[int(path[1])].draw()
                resp = "CONT"
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
