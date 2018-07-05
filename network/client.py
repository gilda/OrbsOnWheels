from http.client import *

class Client():
    # initiates the connection
    def __init__(self, conn):
        self.conn = conn

    # sends get response to connection and prints the response 
    def sendGet(self):
        # send request
        self.conn.request("GET", "/")
        
        # get and print response
        resp = self.conn.getresponse()
        print(resp.status, resp.reason)
        print(resp.read())

    def sendPOST(self, data):
        # send request
        self.conn.request("POST", "/", data)

        # get and print response
        resp = self.conn.getresponse()
        print(resp.status, resp.reason)
        print(resp.read())

def main():
    connection = Client(HTTPConnection("169.254.1.234", 80))
    connection.sendPOST("GILDA IS POSTING SMTH")

if __name__ == "__main__":
    main()
