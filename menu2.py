import termcolor
import socket
import http.server
import socketserver
import atexit
import os
import shutil
import curses
import readline
import rlcompleter
import datetime
import threading
import multiprocessing
import logging
import sys
import sqlite3
import queue
from cmd import Cmd
from termcolor import colored
from threading import Thread



from backend.TCPlistener import tcplistener
from backend.HTTPlistener import httplistener

from backend.Interact import interacting, HTTPinteracting
#from backend.HTTPshandler import http_sHandler



TCPListenersDict = {}
TCPConnectionsDict = {}
TCPprocesses = []

HTTPListenersDict = {}
HTTPConnectionsDict = {}
HTTPprocesses = []

HTTPSListenersDict = {}
HTTPSConnectionsDict = {}
HTTPSprocesses = []


#sockets = []
#TCPSocketDict = {}

manager = multiprocessing.Manager()

TCPreturn_dict = manager.dict()
TCPSocketDict = manager.dict()

HTTPmanager = multiprocessing.Manager()

HTTPreturn_dict = HTTPmanager.dict()
HTTPserverDict = HTTPmanager.dict()

HTTPSmanager = multiprocessing.Manager()

HTTPSreturn_dict = HTTPSmanager.dict()
HTTPSserverDict = HTTPSmanager.dict()


#comment/uncomment the line underneath to have debug log displayed/not displayed
logging.basicConfig(level=logging.DEBUG)

class Commands(Cmd):
    # reguraly check if TCPlistener received a connection
    def TCPcheck4incoming():
        while True:
            if len(TCPreturn_dict) != 0 :
                NAME = TCPreturn_dict.get("name")
                if  NAME in TCPSocketDict:
                    continue
                else:
                    TCPSocketDict[NAME]=TCPreturn_dict.get("conn")
                    TCPListenersDict[NAME][3] = str(TCPreturn_dict.get("status"))
                    TCPConnectionsDict.setdefault(NAME, []).append(TCPreturn_dict.get("host"))
                    TCPConnectionsDict.setdefault(NAME, []).append(TCPreturn_dict.get("port"))
                    TCPConnectionsDict.setdefault(NAME, []).append(TCPreturn_dict.get("name"))
                    addr = TCPreturn_dict.get("addr")
                    TCPConnectionsDict.setdefault(NAME, []).append(addr[0])
                    TCPConnectionsDict.setdefault(NAME, []).append(addr[1])

    T = Thread(target = TCPcheck4incoming, args=())
    T.setDaemon(True)
    T.start()


    def HTTPcheck4incoming():
        while True:
            if len(HTTPreturn_dict) != 0 :
                NAME = HTTPreturn_dict.get("name")
                if  NAME in HTTPserverDict:
                    continue
                else:
                    HTTPListenersDict[NAME][3] = str(HTTPreturn_dict.get("status"))
                    host = HTTPreturn_dict.get("host")
                    port = HTTPreturn_dict.get("port")
                    name = HTTPreturn_dict.get("name")
                    status = HTTPreturn_dict.get("status")
                    HTTPserverDict[NAME]=[host, port, name, status]

                    print("dict: ")
                    print(HTTPserverDict)

    HTTPthread = Thread(target = HTTPcheck4incoming, args=())
    HTTPthread.setDaemon(True)
    HTTPthread.start()

    #presentation part
    intro = """
&@@
  #@@@@,
      @@@@@%
          @@@@@@@/
               @@@@@@@@@@
                        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                           @@@@@@@@@@@@@@@@@.      ..     .@@@@
                              @@@@@@@@@@@@@.    %##[]##%    .@@@@
                                 @@@@@@@@@.    %.%&[]&%.%   .@@@@@@
                                    &@@@@@.     %##[]##%    .@@@@@@@@@
                                       %@@@.       ..      .@@@@@@@@@@@@&
                                          &@@.           .@@@@@@@@@@@@@@@@@
                                              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                                                                          @@@@@@@%
                                                                                /@@@@
                                                                                     &@#
            """
    intro = intro.replace('#', termcolor.colored('#', 'red'))
    intro = intro.replace('[]', termcolor.colored('[]', 'grey'))
    intro = intro.replace('&', termcolor.colored('&', 'red'))
    intro = intro.replace('%', termcolor.colored('%', 'red'))
    intro = intro.replace('.', termcolor.colored('.', 'blue'))
    print(intro)

    while True:


        Datetime = datetime.datetime.now()
        Datetime = Datetime.strftime(colored('%d-%b-%Y_%I', "green")+':'+ colored('%M%p', "green"))


        prompt = Datetime+":kaleidoscope"+">>>"
        prompt = prompt.replace('kaleidoscope', termcolor.colored('kaleidoscope', 'red'))
        prompt = prompt.replace(':', termcolor.colored(':', 'blue'))
        prompt = prompt.replace('>>>', termcolor.colored('>>>', 'blue'))
        prompt = prompt.replace(Datetime, termcolor.colored(Datetime, 'green'))

        command = input(prompt)





        #part responsible for command history and autoComplete
        #work only on unix
        storeCommandPath = os.path.expanduser("./history/k_Command_history")

        if os.path.exists(storeCommandPath):
            readline.read_history_file(storeCommandPath)
        #save command history at close
        def saveCommand(storeCommandPath=storeCommandPath):
            readline.write_history_file(storeCommandPath)

        atexit.register(saveCommand)
        #link tab for auto complete
        readline.parse_and_bind('tab: complete')

        # #this if loop verify if the database already exist if it doesn't it create one
        # #as well as a table
        # if os.path.exists("database/HTTPlistener.db") == False:
        #     conn = sqlite3.connect('database/HTTPlistener.db')
        #     c = conn.cursor()
        #     logging.debug("HTTPlistener.db has been created")
        #
        #     c.execute("""CREATE TABLE HTTPlistener (
        #                 hostIP text,
        #                 hostPORT text,
        #                 name text,
        #                 targetIP,
        #                 targetPORT,
        #                 targetHOSTNAME,
        #                 ItemUniqueID
        #                 )""")
        # #if it exist then it just connect to it and create a cursor
        # else:
        #     logging.debug("HTTPlistener.db exist \n")
        #     conn = sqlite3.connect('HTTPlistener.db')
        #     c = conn.cursor()







        if command == "":
            continue
