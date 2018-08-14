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
        print(resp.status, resp.reason)
        print(resp.read())


def main():
    car0 = Car(0, 0.2, 0.2, 0.1)
    connection = Client(HTTPConnection("127.0.0.1", 4590))
    connection.sendGET("/"+str(car0.id)+"/phase")
    connection.sendPOST("/"+str(car0.id)+"/update", carToJson(car0))

    car1 = Car(1, 0.3, 0.3, 0.1)
    connection = Client(HTTPConnection("127.0.0.1", 4590))
    connection.sendGET("/"+str(car1.id)+"/phase")
    connection.sendPOST("/"+str(car1.id)+"/update", carToJson(car1))

    car2 = Car(2, 0.4, 0.4, 0.1)
    connection = Client(HTTPConnection("127.0.0.1", 4590))
    connection.sendGET("/"+str(car2.id)+"/phase")
    connection.sendPOST("/"+str(car2.id)+"/update", carToJson(car2))

    input("Update car 3?\n")
    car2.x = 0.8
    car2.y = 0.8
    connection.sendPOST("/"+str(car2.id)+"/update", carToJson(car2))


if __name__ == "__main__":
    main()
