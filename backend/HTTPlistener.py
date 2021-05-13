import socket
import socketserver
import os
import ctypes
import shutil
from http.server import HTTPServer
from flask import Flask
from flask import request
from flask import render_template
from flask_sockets import Sockets

#from backend.HTTPshandler import http_sHandler
from API.api import runApi
path  = os.getcwd()


class httplistener():

    def __init__(self, hostip, port, name):
        self.HOST = hostip
        self.PORT = port
        self.NAME = name


    def listenerhttp(self, HTTPreturn_dict):
        #print(path)
        shutil.copy(path+'/API/templates/basicTemplates.html', path+'/API/templates/'+self.NAME+'.html')
        HTTPreturn_dict["name"]=self.NAME
        HTTPreturn_dict["status"]="online"
        HTTPreturn_dict["host"]=self.HOST
        HTTPreturn_dict["port"]=self.PORT
        print(HTTPreturn_dict)
        runApi(self.HOST, self.PORT) # star the flask server
