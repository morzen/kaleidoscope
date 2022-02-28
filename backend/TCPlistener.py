import socket
import sqlite3
import http.server
import socketserver
import logging
import threading
import time
import multiprocessing
import logging
import subprocess
import os
from termcolor import colored
from flask import Flask
from http.server import BaseHTTPRequestHandler,HTTPServer

from db_controller import DBcontroller


#comment/uncomment the line underneath to have debug log displayed/not displayed
logging.basicConfig(level=logging.DEBUG)





class tcplistener:
    # init is basically the blue print for our obecjt essential data will be avaible here
    def __init__(self, hostip, port, name, ID):
        self.HOST = hostip
        self.PORT = int(port)
        self.NAME = name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ID = ID


    def listenertcp(self, return_dict):
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen()
        conn, addr = self.sock.accept()
        with conn:
            logging.debug('\nconn: %s', conn)
            print(colored("\n"+self.NAME+"("+self.HOST+":"+str(self.PORT)+")"+" received and answer from "+str(addr), "red"))
            #return data when connection is made in TCPreturn_dict see menu.py
            return_dict["conn"] = conn
            return_dict["selfID"] = str(self.ID)
            targetip = str(addr[0])
            targetport = str(addr[1])

            DBcontroller().tcplistenerDBscriptAdd("connected", targetip, targetport, self.ID)


    def closetcpListener(self):
        self.sock.close()
        print("closed")
        logging.debug("closing listener")
