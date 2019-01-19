import socket
import time
import sys
import threading
import socketserver

otgwHost = "localhost"
otgwPort = 9001
clients = []

class Forwarder:
    input_list = []
    channel = {}

    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.connect((otgwHost, otgwPort))
        self.fp = self.server.makefile('r', buffering=1)

    def main_loop(self):
        self.input_list.append(self.server)
        while True:
            ll = self.fp.readline(100000)
            print("line = {0} ({1} clients)".format(ll, len(clients)))
            for client in clients:
                print("send to client")
                client.writeToClient(bytes(ll, 'utf8'))

class ThreadedTCPRequestHandler(socketserver.StreamRequestHandler):
    def writeToClient(self, s):
        self.wfile.write(s)

    def handle(self):
        print("handle(...)")
        self.writeToClient(bytes('aap', 'utf8'))
        clients.append(self)
        print("#clients = {}".format(len(clients)))
        while True:
            data = self.rfile.readline(10000)
            if len(data) == 0:
                break
            print("d = {0}".format(data))
            server.server.send(data)

        #self.request.sendall(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == '__main__':
    print("start forwarder")

    HOST, PORT = "localhost", 9002

    forwardServer = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with forwardServer:
        ip, port = forwardServer.server_address
        print("listen on {0}:{1}".format(ip, port))

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=forwardServer.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print("Server loop running in thread:", server_thread.name)

        server = Forwarder(otgwHost, otgwPort)
        try:
            server.main_loop()
        except KeyboardInterrupt:
            print("Ctrl C - Stopping server")
            forwardServer.shutdown()
            sys.exit(1)

