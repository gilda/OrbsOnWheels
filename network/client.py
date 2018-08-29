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
        #print(resp.status, resp.reason)
        # print(resp.read())

    def sendPOST(self, path, data):
        # send request
        self.conn.request("POST", path, data)

        # get and print response
        resp = self.conn.getresponse()
        response = resp.read()
        #print(resp.status, resp.reason, path)
        # tell car to parse(response).execute()
        # print(response)
        return response


USE_SERVER_COMMANDS = False


cmd0 = ""
cmd1 = ""
cmd2 = ""

cmd0Input = ["WAIT 100", "ROT 30", "MOVXY 0.5 0.3", "WAIT 30", "ROT 180"]
cmd0Index = 0

cmd1Input = ["ROT 30", "MOVXY 0.8 0.8", "MOVXY 0.2 0.3", "WAIT 30"]
cmd1Index = 0


def main():
    global cmd0
    global cmd1
    global cmd1

    global cmd0Index
    global cmd0Input
    global cmd1Index
    global cmd1Input
    global cmd2Index
    global cmd2Input

    car0 = Car(0, 0.5, 0.5, 0.1, None)
    car0.setVelocity(0.005)

    connection = Client(HTTPConnection("127.0.0.1", 4590))
    connection.sendGET("/"+str(car0.id)+"/phase")
    cmd0 = connection.sendPOST(
        "/"+str(car0.id)+"/update", carToJson(car0)).decode("utf-8").split(" ")

    car1 = Car(1, 0.4, 0.4, 0.1, None)
    car1.setVelocity(0.005)

    connection = Client(HTTPConnection("127.0.0.1", 4590))
    connection.sendGET("/"+str(car1.id)+"/phase")
    cmd1 = connection.sendPOST(
        "/"+str(car1.id)+"/update", carToJson(car1)).decode("utf-8").split(" ")

    car2 = Car(2, 0.2, 0.6, 0.1, None)
    car2.setVelocity(0.005)

    connection = Client(HTTPConnection("127.0.0.1", 4590))
    connection.sendGET("/"+str(car2.id)+"/phase")
    cmd2 = connection.sendPOST(
        "/"+str(car2.id)+"/update", carToJson(car2)).decode("utf-8").split(" ")

    if USE_SERVER_COMMANDS:
        input("start simulating?\n")
        time.sleep(3)
        while True:

            if cmd0[0] == "ROT":
                car0.rotate(int(cmd0[1]))
            elif cmd0[0] == "MOV":
                car0.move()
            elif cmd0[0] == "MOVXY":
                car0.move_xy(float(cmd0[1]), float(cmd0[2]))
            elif cmd0[0] == "RAD":
                car0.move_rad(float(cmd0[1]), float(cmd0[2]))
            elif cmd0[0] == "WAIT":
                if car0.interval == 0 or car0.interval == None:
                    car0.wait(int(cmd0[1]))
            else:
                print("No such command")
            car0.decInterval()

            if cmd1[0] == "ROT":
                car1.rotate(int(cmd1[1]))
            elif cmd1[0] == "MOV":
                car1.move()
            elif cmd1[0] == "MOVXY":
                car1.move_xy(float(cmd1[1]), float(cmd1[2]))
            elif cmd1[0] == "RAD":
                car1.move_rad(float(cmd1[1]), float(cmd1[2]))
            elif cmd1[0] == "WAIT":
                if car1.interval == 0 or car1.interval == None:
                    car1.wait(int(cmd1[1]))
            else:
                print("No such command")
            # draw the car after all changes were made
            car1.decInterval()

            if cmd2[0] == "ROT":
                car2.rotate(int(cmd2[1]))
            elif cmd2[0] == "MOV":
                car2.move()
            elif cmd2[0] == "MOVXY":
                car2.move_xy(float(cmd2[1]), float(cmd2[2]))
            elif cmd2[0] == "RAD":
                car2.move_rad(float(cmd2[1]), float(cmd2[2]))
            elif cmd2[0] == "WAIT":
                if car2.interval == 0 or car2.interval == None:
                    car2.wait(int(cmd2[1]))
            else:
                print("No such command")
            car2.decInterval()

            # send all of the cars data to the server for simulation to display
            connection = Client(HTTPConnection("127.0.0.1", 4590))
            connection.sendGET("/"+str(car0.id)+"/phase")
            cmd0 = connection.sendPOST(
                "/"+str(car0.id)+"/update", carToJson(car0)).decode("utf-8").split(" ")

            connection = Client(HTTPConnection("127.0.0.1", 4590))
            connection.sendGET("/"+str(car1.id)+"/phase")
            cmd1 = connection.sendPOST(
                "/"+str(car1.id)+"/update", carToJson(car1)).decode("utf-8").split(" ")

            connection = Client(HTTPConnection("127.0.0.1", 4590))
            connection.sendGET("/"+str(car2.id)+"/phase")
            cmd2 = connection.sendPOST(
                "/"+str(car2.id)+"/update", carToJson(car2)).decode("utf-8").split(" ")

            time.sleep(0.01)
    else:
        while True:
            # change and ask for new state only if the current state is stop
            # meaning that ll current commands were accomplished
            if car0.state == None or car0.state == car0.stop:
                if cmd0Index <= len(cmd0Input) - 1:
                    cmd0 = cmd0Input[cmd0Index]
                    cmd0Index += 1
                    cmd0 = cmd0.split(" ")

            car0.parseCommand(cmd0)
            # decrease car wait time interval
            car0.decInterval()

            # change and ask for new state only if the current state is stop
            # meaning that all current commands were accomplished
            if car1.state == None or car1.state == car1.stop:
                if cmd1Index <= len(cmd1Input) - 1:
                    cmd1 = cmd1Input[cmd1Index]
                    cmd1Index += 1
                    cmd1 = cmd1.split(" ")

            car1.parseCommand(cmd1)
            # draw the car after all changes were made
            car1.decInterval()

            # change and ask for new state only if the current state is stop
            # meaning that ll current commands were accomplished
            if car2.state == None or car2.state == car2.stop:
                if cmd2Index <= len(cmd2Input) - 1:
                    cmd2 = cmd2Input[cmd2Index]
                    cmd2Index += 1
                    cmd2 = cmd2.split(" ")

            car2.parseCommand(cmd2)
            car2.decInterval()

            # send all of the cars data to the server for simulation to display
            connection = Client(HTTPConnection("127.0.0.1", 4590))
            connection.sendGET("/"+str(car0.id)+"/phase")
            connection.sendPOST("/"+str(car0.id)+"/update",
                                carToJson(car0)).decode("utf-8").split(" ")

            connection = Client(HTTPConnection("127.0.0.1", 4590))
            connection.sendGET("/"+str(car1.id)+"/phase")
            connection.sendPOST("/"+str(car1.id)+"/update",
                                carToJson(car1)).decode("utf-8").split(" ")

            connection = Client(HTTPConnection("127.0.0.1", 4590))
            connection.sendGET("/"+str(car2.id)+"/phase")
            connection.sendPOST("/"+str(car2.id)+"/update",
                                carToJson(car2)).decode("utf-8").split(" ")

            time.sleep(0.01)


if __name__ == "__main__":
    main()
