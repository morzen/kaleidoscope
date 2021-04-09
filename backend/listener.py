import socket
import http.server
import socketserver
import logging
import threading
import threading
import time
import logging
import subprocess
import os
import datetime
from termcolor import colored
from flask import Flask

#comment/uncomment the line underneath to have debug log displayed/not displayed
logging.basicConfig(level=logging.DEBUG)

Datetime = datetime.datetime.now()
Datetime = Datetime.strftime(colored('%d-%b-%Y_%I', "green")+':'+ colored('%M%p', "green"))


class listener:

    def __init__(self, hostip, port, name):
        self.HOST = hostip
        self.PORT = port
        self.NAME = name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    def Simplelistener(self):
        #print("I am a Simple listener")
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen()
        conn, addr = self.sock.accept()
        with conn:
            logging.debug('\nconn: %s', conn)



    def closeSimpleListener(self):
        self.sock.close()
        logging.debug("closing listener")



    def checkPortNIPfree(self, hostip, port):
        HOST = hostip
        PORT = port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        # try:
        #     s.bind((HOST, PORT))
        #     return True
        # except:
        #     return False
        s.close()

    def listenerHTTP(self, hostip, port):

        HOST = hostip
        PORT = port

        Handler = http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
            print("host: "+HOST+" serving at port", PORT)
            httpd.serve_forever()

    #temporary function just for testing purposes
    def client():
        logging.debug("client")
        HOST = '127.0.0.1'
        PORT = 65432

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall('Hello, world'.encode())
            data = s.recv(1024)

        print('Received', repr(data))
