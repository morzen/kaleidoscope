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

    def interact(self, hostip, port):
        HOST = hostip
        PORT = port

        while True:
            cmd = input(Datetime+"_"+HOST+":"+str(PORT)+">> ")

            if cmd == "exit":
                self.closeConnection(HOST, PORT)



    def closeConnection(hostip, port):
        HOST = hostip
        PORT = port

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            conn.close()
            s.close()
