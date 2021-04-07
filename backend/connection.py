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

class connection:

    def __init__(self, hostip, port, name):
        self.HOST = hostip
        self.PORT = port
        self.NAME = name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.HOST, self.PORT))

    def interactWith(self):
        HOST = self.HOST
        PORT = self.PORT

        while True:
            cmd = input(Datetime+"_"+HOST+":"+str(PORT)+">> ")

            if cmd == "exit":
                self.sock.closeConnection(HOST, PORT)



    def closeConnection(self):
        conn, addr = self.sock.accept()
        conn.close()
        self.sock.close()
