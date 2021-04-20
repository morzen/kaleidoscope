import socket
import socketserver
from flask import Flask
from flask import request
from flask import render_template
from flask_sockets import Sockets

app = Flask(__name__)
app.debug = True

sockets = Sockets(app)

class httplistener():

    def __init__(self, hostip, port, name):
        self.HOST = hostip
        self.PORT = port
        self.NAME = name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock.setblocking(False)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    @app.route('/')
    def startpage(self):
        print("2")
        print(self.HOST)
        return render_template('index.html', rp=rp)
        print("3")
        # with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
        #     print("host: "+HOST+" serving at port", PORT)
        #     httpd.serve_forever()

    def run(self):
        app.run(host=self.HOST, port=self.PORT)
