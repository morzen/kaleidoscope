import socket
import socketserver
import os
import ctypes
import logging
import shutil
from http.server import HTTPServer
from flask import Flask
from flask import request
from flask import render_template
from flask_sockets import Sockets

#from backend.HTTPshandler import http_sHandler
from API.api import runApi
from API.api import runApiSSL
path  = os.getcwd()

#comment/uncomment the line underneath to have debug log displayed/not displayed
logging.basicConfig(level=logging.DEBUG)

class httplistener():
    #init create the object it is composed of all the variable that would be
    #needed for this object
    def __init__(self, hostip, port, name, ID, *certnkey):
        self.HOST = hostip
        self.PORT = port
        self.NAME = name
        self.CERTnKeyPath = (certnkey)



    def listenerhttp(self, HTTPreturn_dict):
        #logging.debug(path)
        #create a new html file PAGES ARE DYNAMICALLY GENERATED HERE (uses /basicTemplates.html)
        shutil.copy(path+'/API/templates/basicTemplates.html', path+'/API/templates/'+self.NAME+'.html')
        # since we are creating a server the data is returned straight away
        #status is online since in all likelyhood no connection has been made
        #we just started the server
        HTTPreturn_dict["name"]=self.NAME
        HTTPreturn_dict["status"]="online"
        HTTPreturn_dict["host"]=self.HOST
        HTTPreturn_dict["port"]=self.PORT
        conn = sqlite3.connect('listener.db')
        c = conn.cursor()
        c.execute("UPDATE HTTP/Slistener SET targetIP=? WHERE ItemUniqueID=?", ("online", ID))
        conn.commit()
        #logging.debug(HTTPreturn_dict)
        runApi(self.HOST, self.PORT) # star the flask server

    def listenerhttps(self, HTTPreturn_dict):
        #logging.debug(path)
        shutil.copy(path+'/API/templates/basicTemplates.html', path+'/API/templates/'+self.NAME+'.html')
        HTTPreturn_dict["name"]=self.NAME
        HTTPreturn_dict["status"]="online"
        HTTPreturn_dict["host"]=self.HOST
        HTTPreturn_dict["port"]=self.PORT

        conn = sqlite3.connect('listener.db')
        c = conn.cursor()
        c.execute("UPDATE HTTP/Slistener SET targetIP=? WHERE ItemUniqueID=?", ("online", ID))
        conn.commit()

        runApiSSL(self.HOST, self.PORT, self.CERTnKeyPath) # start the flask server
