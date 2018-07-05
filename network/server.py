from http.server import *

class Server(BaseHTTPRequestHandler):
    
    def do_GET(self):
        # print all parameters        
        print(self.path)
        print(self.headers)

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

def main():
    httpd = HTTPServer(("127.0.0.1", 80), Server)
    httpd.serve_forever()

if __name__ == "__main__":
    main()