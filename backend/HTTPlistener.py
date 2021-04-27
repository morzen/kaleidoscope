import socket
import socketserver
import ctypes
from http.server import HTTPServer
from flask import Flask
from flask import request
from flask import render_template
from flask_sockets import Sockets

from backend.HTTPshandler import http_sHandler
#from API.api import runApi

class httplistener():

    def __init__(self, hostip, port, name):
        self.HOST = hostip
        self.PORT = port
        self.NAME = name
        self.Handler = http_sHandler


    def listenerhttp(self, return_dict):
        Hostaddress = (self.HOST, self.PORT)
        httpd = HTTPServer(Hostaddress, self.Handler)


        #return_dict["httplistener"]=httpd
        return_dict["name"]=self.NAME
        return_dict["status"]="connected"
        return_dict["host"]=self.HOST
        return_dict["port"]=self.PORT
        httpd.serve_forever()


        #httpd.server_close()

    # def listenerhttp(self, return_dict):
    #     httpserver = runApi(self.HOST, int(self.PORT))
    #
    #     return_dict["httplistener"]=httpserver
    #     return_dict["name"]=self.NAME
    #     return_dict["status"]="online"
    #     return_dict["host"]=self.HOST
    #     return_dict["port"]=self.PORT
    #
    #     return httpserver
