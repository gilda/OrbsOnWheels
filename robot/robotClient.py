from http.client import *
from car import *
import time


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

# TODO implement recieve command
def recieveExecute():
    pass

def sendUpdate(car):
    connection = Client(HTTPConnection("127.0.0.1", 4590))
    connection.sendGET("/"+str(car.id)+"/phase")
    connection.sendPOST("/"+str(car.id)+"/update", carToJson(car))

