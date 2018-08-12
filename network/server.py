from http.server import *
from network.car import *
import time

game = None

def main():
    global game
    game = Game(3, [])
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

    def do_GET(self):
        global cars
        global game
        # print all parameters        
        print(self.path)
        #print(self.headers)

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
            if not path[1] in game.ready:
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
            
            # update car in game.cars list
            print(data)
            game.cars[int(path[1])] = jsonToCar(data)

            # response code for response
            self.send_response(200)
            # add all headers for response
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # write to output file the message content
            self.wfile.write(bytes(resp, "utf-8"))
            return

if __name__ == "__main__":
    main()
