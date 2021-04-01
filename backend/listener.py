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

    def checkPortNIPfree(self, hostip, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            try:
                sock.bind((HOST, PORT))
                return True
            except:
                return False
            sock.close()

    def Simplelistener(self, hostip, port, name):
        logging.debug("listener")
        HOST = hostip
        PORT = port

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            connection = name + conn
            with conn:
                print('listner:'+name+' addr:', addr+ 'received connection')
                print('conn:', conn)
        return connection

    def listenerHTTP(self, hostip, port):

        HOST = hostip
        PORT = port

        Handler = http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
            print("host: "+HOST+" serving at port", PORT)
            httpd.serve_forever()

    def closeSimpleListener(self, hostip, port):
        HOST = hostip
        PORT = port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            print("closed")
            s.close()



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
