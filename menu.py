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

from backend.Interact import interacting
#from backend.HTTPshandler import http_sHandler



TCPListenersDict = {}
TCPConnectionsDict = {}
TCPprocesses = []

HTTPListenersDict = {}
HTTPConnectionsDict = {}
HTTPprocesses = []


#sockets = []
#TCPSocketDict = {}

manager = multiprocessing.Manager()

TCPreturn_dict = manager.dict()
TCPSocketDict = manager.dict()

HTTPreturn_dict = manager.dict()
HTTPserverDict = manager.dict()


#comment/uncomment the line underneath to have debug log displayed/not displayed
logging.basicConfig(level=logging.DEBUG)

class Commands(Cmd):

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


    Datetime = datetime.datetime.now()
    Datetime = Datetime.strftime(colored('%d-%b-%Y_%I', "green")+':'+ colored('%M%p', "green"))


    prompt = Datetime+":kaleidoscope"+">>>"
    prompt = prompt.replace('kaleidoscope', termcolor.colored('kaleidoscope', 'red'))
    prompt = prompt.replace(':', termcolor.colored(':', 'blue'))
    prompt = prompt.replace('>>>', termcolor.colored('>>>', 'blue'))
    prompt = prompt.replace(Datetime, termcolor.colored(Datetime, 'green'))

    #print(dataandtime[0])





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

    # reguraly check if TCPlistener received a connection
    def HTTPcheck4incoming():
        while True:
            if len(HTTPreturn_dict) != 0 :
                NAME = HTTPreturn_dict.get("name")
                if  NAME in HTTPserverDict:
                    continue
                else:
                    HTTPserverDict[NAME]=HTTPreturn_dict.get("httplistener")
                    HTTPListenersDict[NAME][3] = str(HTTPreturn_dict.get("status"))
                    HTTPConnectionsDict.setdefault(NAME, []).append(HTTPreturn_dict.get("host"))
                    HTTPConnectionsDict.setdefault(NAME, []).append(HTTPreturn_dict.get("port"))
                    HTTPConnectionsDict.setdefault(NAME, []).append(HTTPreturn_dict.get("name"))


    HTTPthread = Thread(target = HTTPcheck4incoming, args=())
    HTTPthread.setDaemon(True)
    HTTPthread.start()




    def emptyline(self):
        pass

    #command part

    def do_tcplistener(self, inp):
        #try:

        argList = []
        argList = inp.split()
        HOST = argList[0]
        PORT = int(argList[1])
        NAME = argList[2]
        STATUS = "listening"
        TCPListenersDict.setdefault(NAME, []).append(HOST)
        TCPListenersDict.setdefault(NAME, []).append(PORT)
        TCPListenersDict.setdefault(NAME, []).append(NAME)
        TCPListenersDict.setdefault(NAME, []).append(STATUS)
        ListenerCreation = tcplistener(HOST, PORT, NAME)

        p = multiprocessing.Process(name=NAME ,target=ListenerCreation.listenertcp, args=[TCPreturn_dict])
        TCPprocesses.append(p)
        print(TCPprocesses)
        p.start()


        # except:
        #     print(colored("-error: did you corretly enter the argument?", "red"))
        #     print(colored("example: tcplistener hostip port", "yellow"))
        #     print(colored("example: tcplistener 127.0.0.1 8080", "yellow"))

    def do_HTTPlistener(self, inp):
        argList = []
        argList = inp.split()
        HOST = argList[0]
        PORT = int(argList[1])
        NAME = argList[2]
        STATUS = "listening"
        HTTPListenersDict.setdefault(NAME, []).append(HOST)
        HTTPListenersDict.setdefault(NAME, []).append(PORT)
        HTTPListenersDict.setdefault(NAME, []).append(NAME)
        HTTPListenersDict.setdefault(NAME, []).append(STATUS)

        HTTPListenerCreation = httplistener(HOST, PORT, NAME)

        p = multiprocessing.Process(name=NAME ,target=HTTPListenerCreation.listenerhttp, args=[HTTPreturn_dict])
        HTTPprocesses.append(p)
        print(HTTPprocesses)
        #p.daemon = True
        p.start()



    def do_interact(self, inp):
        argList = []
        argList = inp.split()
        name = argList[0]

        info = TCPConnectionsDict.get(name)
        print(TCPSocketDict)

        HOST = info[3]
        PORT = info[4]
        NAME = info[2]
        Conn = TCPSocketDict[NAME]

        InteractWith = interacting(HOST, int(PORT), NAME, Conn)
        while True:
            try1 = InteractWith.Shell()
            if try1 == False:
                break

            elif try1 == "Close Connection":
                i = 0
                print(NAME)
                j = None
                LenTCPprocesses = len(TCPprocesses)
                while i < LenTCPprocesses:
                    if NAME in str(TCPprocesses[i]):
                        print(NAME+" is in "+str(TCPprocesses[i]))
                        j = str(i)
                    else:
                        print(NAME+" is not in "+str(TCPprocesses[i]))

                    i = i + 1
                print("j="+j)
                p = TCPprocesses[int(j)]
                del TCPprocesses[int(j)]
                TCPListenersDict.pop(NAME)
                p.terminate()

                break

            else:
                continue

    #def do_HTTPinteract(self, inp):


    def do_listListener(self, inp):
        print(TCPListenersDict)

        print("\n HTTPserverDict: ")
        print(HTTPserverDict)

    def do_listConnections(self, inp):
        print(TCPConnectionsDict)
        print(TCPreturn_dict)
        # conn = TCPreturn_dict.get("conn")
        # msg = conn.recv(1024).decode()
        # print("\nmessage: "+msg)

    def do_close_listener(self, inp):

        argList = []
        argList = inp.split()
        name = argList[0]
        info = TCPListenersDict[name]
        infoSplitList = info.split()
        HOST = infoSplitList[0]
        PORT = infoSplitList[1]
        NAME = infoSplitList[2]
        ListenerClose = listener(HOST,int(PORT), NAME)

        ListenerClose.closetcpListener()
        i = 0
        print(NAME)
        j = None
        LenTCPprocesses = len(TCPprocesses)
        while i < LenTCPprocesses:
            if NAME in str(TCPprocesses[i]):
                #print(NAME+" is in "+str(TCPprocesses[i]))
                logging.debug(NAME+" is in "+str(TCPprocesses[i]))
                j = str(i)
            else:
                #print(NAME+" is not in "+str(TCPprocesses[i]))
                logging.debug(NAME+" is not in "+str(TCPprocesses[i]))
            i = i + 1
        logging.debug("j= %s", j)
        p = TCPprocesses[int(j)]
        del TCPprocesses[int(j)]
        TCPListenersDict.pop(NAME)
        TCPConnectionsDict.pop(NAME)
        p.terminate()

    def do_close_HTTPlistener(self, inp):
        path  = os.getcwd()
        argList = []
        argList = inp.split()
        NAME = argList[0]
        i = 0
        j = None
        LenHTTPprocesses = len(HTTPprocesses)
        while i < LenHTTPprocesses:
            if NAME in str(HTTPprocesses[i]):
                logging.debug(NAME+" is in "+str(HTTPprocesses[i]))
                j = str(i)
            else:
                logging.debug(NAME+" is not in "+str(HTTPprocesses[i]))
            i = i + 1
        logging.debug("j= %s", j)
        p = HTTPprocesses[int(j)]
        del HTTPprocesses[int(j)]
        HTTPListenersDict.pop(NAME)
        try:
            HTTPConnectionsDict.pop(NAME)
        except:
            print('error http delete item in HTTPConnectionsDict' )
            print(HTTPConnectionsDict)
        p.terminate()
        os.unlink(path+'/API/templates/'+NAME+'.html')

    def do_clear(self, inp):
        clear = lambda: os.system('clear')
        clear()

    def do_exit(self, inp):
        #exit()
        #T.close()
        sys.exit("shut me down and i will become more \npowerfull than you can possibly imagine.")
        quit()


Commands().cmdloop()
