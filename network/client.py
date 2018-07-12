from http.client import *

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
    connection = Client(HTTPConnection("127.0.0.1", 4590))
    connection.sendGET("/gamePhase")

if __name__ == "__main__":
    main()
