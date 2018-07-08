from http.server import *
from car import *
import matplotlib.pyplot as plt
import json

class Server(BaseHTTPRequestHandler):
    
    global cars

    def do_GET(self):
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
            self.wfile.write(cartoJson(cars[0]))
            
            return

        # response code for response
        self.send_response(200)

        # add all headers for response
        self.send_header("Content-type","text/html")
        self.end_headers()

        # write to output file the message content
        self.wfile.write(bytes("Gilda has an HTTP server!", "utf-8"))
        return
    
    def do_POST(self):
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

def cartoJson(car):
    return bytes(json.dumps({"id": car.id,
                        "pos": {"x": car.x,
                                "y": car.y,
                                "angle": car.angle}}, indent=4, sort_keys=True), "utf-8")

cars = [Car(0, 0, 0, 0.1, plt.Polygon(calcTriangle(0, 0.1), closed=True, facecolor="red"))]

httpd = HTTPServer(("0.0.0.0", 80), Server)
httpd.serve_forever()


def main():
    pass

if __name__ == "__main__":
    main()
