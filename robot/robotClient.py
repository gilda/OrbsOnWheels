from http.client import *
from robotCar import *
import time

HOST = "127.0.0.1"
PORT = 4590


class Client():
    # initiates the connection
    def __init__(self, conn):
        self.conn = conn

    # sends get response to connection and prints the response
    def sendGET(self, path):
        # send request
        self.conn.request("GET", path)

        # get and print response
        resp = self.conn.getresponse()
        print(resp.status, resp.reason)
        print(resp.read())

    def sendPOST(self, path, data):
        # send request
        self.conn.request("POST", path, data)

        # get and print response
        resp = self.conn.getresponse()
        response = resp.read()
        print(resp.status, resp.reason)
        # tell car to parse(response).execute()
        print(response)
        return response

# TODO implement recieve command using ORBS
# execute using a new thread and thread.start() doesn't have to include a variable
# make sure to have always a way to stop the car.


def recieveCommand():
    pass

# send a phase command to the server. like a stay alive message


def sendPhase(car):
    connection = Client(HTTPConnection(HOST, PORT))
    connection.sendGET("/"+str(car.id)+"/phase")

# send the car's coordinates and ID to the server


def sendUpdate(car):
    connection = Client(HTTPConnection(HOST, PORT))
    connection.sendGET("/"+str(car.id)+"/phase")
    resp = connection.sendPOST("/"+str(car.id)+"/update", carToJson(car))
    return resp
