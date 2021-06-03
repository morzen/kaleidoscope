import socket
import sqlite3
import http.server
import socketserver
import logging
import threading
import threading
import time
import multiprocessing
import logging
import subprocess
import os
import datetime
from termcolor import colored
from flask import Flask
from http.server import BaseHTTPRequestHandler,HTTPServer



#comment/uncomment the line underneath to have debug log displayed/not displayed
logging.basicConfig(level=logging.DEBUG)

Datetime = datetime.datetime.now()
Datetime = Datetime.strftime(colored('%d-%b-%Y_%I', "green")+':'+ colored('%M%p', "green"))

#app = Flask(__name__)


class tcplistener:
    # init is basically the blue print for our obecjt essential data will be avaible here
    def __init__(self, hostip, port, name):
        self.HOST = hostip
        self.PORT = port
        self.NAME = name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock.setblocking(False)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    def listenertcp(self, return_dict):
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen()
        conn, addr = self.sock.accept()
        with conn:
            logging.debug('\nconn: %s', conn)
            print(colored("\n"+self.NAME+"("+self.HOST+str(self.PORT)+")"+" received and answer from "+str(addr), "red"))
            #return data when connection is made in TCPreturn_dict see menu.py
            return_dict["conn"]=conn
            return_dict["name"]=self.NAME
            return_dict["status"]="connected"
            return_dict["addr"]=addr
            return_dict["host"]=self.HOST
            return_dict["port"]=self.PORT


    def closetcpListener(self):
        self.sock.close()
        logging.debug("closing listener")


    #need to be added when in menu when creating TCP listener
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
