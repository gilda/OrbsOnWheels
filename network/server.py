from http.server import *
from car import *
import json
import time

def main():
    httpd = HTTPServer(("127.0.0.1", 4590), Server)
    httpd.serve_forever()

class Game:
    def __init__(self):
        # game always starts with DELAY
        self.state = "DELAY"

    def updateGamePhase(self):
        # calculate the game phase and update it
        self.state = input("WHAT STATE SHOULD I BE IN?")

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
                self.wfile.write(cartoJson(car)+"\r\n")
            return

        if self.path == "/gamePhase":
            # initiate headers
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # send current state of all the cars
            game.updateGamePhase()
            self.wfile.write(bytes(game.state, "utf-8"))
            return

        return
    
    def do_POST(self):
        global cars
        global game

        # print all parameters
        print(self.path)
        print(self.rfile.read(int(self.headers["Content-length"])))

        # response code for response
        self.send_response(200)

        # add all headers for response
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # write to output file the message content
        self.wfile.write(bytes("Gilda server got you post message", "utf-8"))
        return

# serialize the cars to json format for sending on the network
def cartoJson(car):
    return bytes(json.dumps({"id": car.id,
                        "pos": {"x": car.x,
                                "y": car.y,
                                "angle": car.angle}}, indent=4, sort_keys=False), "utf-8")

cars = [Car(0, 0, 0, 0.1)]
game = Game()

if __name__ == "__main__":
    main()
