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
import uuid
from cmd import Cmd
from termcolor import colored
from threading import Thread
from backend.TCPlistener import tcplistener
from backend.HTTPlistener import httplistener
from backend.Interact import interacting, HTTPinteracting
#from backend.HTTPshandler import http_sHandler


#list related to TCP
TCPListenersDict = {}#stores TCP listener with info
TCPConnectionsDict = {}#store info when listener get a connection
TCPprocesses = []#store processes related to TCP such a lsitener
#(keep listener active when connection)

HTTPListenersDict = {}
HTTPConnectionsDict = {}
HTTPprocesses = []

HTTPSListenersDict = {}
HTTPSConnectionsDict = {}
HTTPSprocesses = []




manager = multiprocessing.Manager()
#return info in a dict for a given listener
TCPreturn_dict = manager.dict()
TCPSocketDict = manager.dict()#store the socket when connection for later interaction

HTTPmanager = multiprocessing.Manager()

HTTPreturn_dict = HTTPmanager.dict()
HTTPserverDict = HTTPmanager.dict()

HTTPSmanager = multiprocessing.Manager()

HTTPSreturn_dict = HTTPSmanager.dict()
HTTPSserverDict = HTTPSmanager.dict()


#comment/uncomment the line underneath to have debug log displayed/not displayed
logging.basicConfig(level=logging.DEBUG)

def MakeNcheckID():
    while True:
        ID = str(uuid.uuid4().fields[-1])[:5]
        conn = sqlite3.connect('database/listener.db')
        c = conn.cursor()
        c.execute("SELECT ItemUniqueID FROM TCPlistener UNION SELECT ItemUniqueID from HTTPsListener")
        IDs = c.fetchall()
        if ID in IDs:
            continue
        else:
            return ID

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
    #the prompt variable used this way seem to block the clock need to be fixed (trying to in menu2)

    prompt = Datetime+":kaleidoscope"+">>>"
    prompt = prompt.replace('kaleidoscope', termcolor.colored('kaleidoscope', 'red'))
    prompt = prompt.replace(':', termcolor.colored(':', 'blue'))
    prompt = prompt.replace('>>>', termcolor.colored('>>>', 'blue'))
    prompt = prompt.replace(Datetime, termcolor.colored(Datetime, 'green'))

    #part responsible for command history and autoComplete
    #work only on unix !!
    #historic stored at the given path here
    storeCommandPath = os.path.expanduser("./history/k_Command_history")

    if os.path.exists(storeCommandPath):
        readline.read_history_file(storeCommandPath)
    def saveCommand(storeCommandPath=storeCommandPath):
        readline.write_history_file(storeCommandPath)

    #save command history at close
    atexit.register(saveCommand)
    #link tab for auto complete
    readline.parse_and_bind('tab: complete')


    #this if loop verify if the database already exist if it doesn't it create one
    #as well as a table
    if os.path.exists("database/listener.db") == True:
        logging.debug("listener.db exist \n")
        conn = sqlite3.connect('database/listener.db')
        c = conn.cursor()
    #if it exist then it just connect to it and create a cursor
    else:
        conn = sqlite3.connect('database/listener.db')
        c = conn.cursor()
        logging.debug("listener.db has been created")

        c.execute("""CREATE TABLE TCPlistener (
                    ItemUniqueID int,
                    hostIP text,
                    hostPORT text,
                    name text,
                    status text,
                    targetIP text,
                    targetPORT text,
                    targetHOSTNAME text,
                    socketconn
                    )""")

        c.execute("""CREATE TABLE HTTPsListener (
                    ItemUniqueID int,
                    hostIP text,
                    hostPORT text,
                    name text,
                    status text,
                    targetIP,
                    targetPORT text,
                    targetHOSTNAME text,
                    SSLcertPath text,
                    SSLkeyPath text
                    )""")
        conn.commit()

    # reguraly check if TCPlistener received a connection
    # endless thread that check for info when a connection is made
    def TCPcheck4incoming():
        while True:
            #check if TCPlistener is not empty
            if len(TCPreturn_dict) != 0 :
                conn = TCPreturn_dict.get("conn")
                ID = TCPreturn_dict.get("selfID")
                if ID not in TCPSocketDict:
                    TCPSocketDict[ID]=conn
                else:
                    continue



    T = Thread(target = TCPcheck4incoming, args=())
    T.setDaemon(True)
    T.start()

    #when nothing is enter insure that the prompt reapear
    def emptyline(self):
        pass

    #command part

    #comand to created TCP listener
    def do_tcplistener(self, inp):
        #try:
        #the arguments from inp are stored in argList
        argList = []
        argList = inp.split()
        #after spliting the list the argument are assigned to variables
        HOST = argList[0]
        PORT = int(argList[1])
        NAME = "TCP_"+argList[2]
        STATUS = "listening"
        ID = MakeNcheckID()
        conn = sqlite3.connect('database/listener.db')
        c = conn.cursor()
        c.execute("INSERT INTO TCPlistener (ItemUniqueID, hostIP, hostPort, name, status) VALUES(?, ?, ?, ?, ?)",
                                      (ID, HOST, PORT, NAME, STATUS))
        conn.commit()
        #creating object an object tcplistener
        ListenerCreation = tcplistener(HOST, PORT, NAME, ID)
        # calling funtion listenertcp from tcplistener in a process
        p = multiprocessing.Process(name=NAME ,target=ListenerCreation.listenertcp, args=[TCPreturn_dict])
        #store the process in a list TCPprocesses
        TCPprocesses.append(p)
        logging.debug(TCPprocesses)
        p.start()


        # except:
        #     print(colored("-error: did you corretly enter the argument?", "red"))
        #     print(colored("example: tcplistener hostip port", "yellow"))
        #     print(colored("example: tcplistener 127.0.0.1 8080", "yellow"))

    #command to create http server that'll listen for incoming connections
    def do_HTTPlistener(self, inp):
        #the arguments from inp are stored in argList
        argList = []
        argList = inp.split()
        #after spliting the list the argument are assigned to variables
        HOST = argList[0]
        PORT = int(argList[1])
        NAME = "HTTP_"+argList[2]
        STATUS = "listening"
        ID = MakeNcheckID()
        #for tracability the information are then stored into a dictionnary
        #regrouping all http listener
        HTTPListenersDict.setdefault(NAME, []).append(HOST)
        HTTPListenersDict.setdefault(NAME, []).append(PORT)
        HTTPListenersDict.setdefault(NAME, []).append(NAME)
        HTTPListenersDict.setdefault(NAME, []).append(STATUS)
        conn = sqlite3.connect('database/listener.db')
        c = conn.cursor()
        c.execute("INSERT INTO HTTPsListener (ItemUniqueID, hostIP, hostPort, name, status) VALUES(?, ?, ?, ?, ?)",
                                      (ID, HOST, PORT, NAME, STATUS))
        conn.commit()
        #creating object an object httplistener
        HTTPListenerCreation = httplistener(HOST, PORT, NAME, ID)
        # calling funtion listenerhttp from httplistener in a process
        p = multiprocessing.Process(name=NAME, target=HTTPListenerCreation.listenerhttp, args=[HTTPreturn_dict])
        #store the process in a list HTTPprocesses
        HTTPprocesses.append(p)
        logging.debug(HTTPprocesses)
        p.start()

    def do_HTTPSlistener(self, inp):
        argList = []
        argList = inp.split()
        HOST = argList[0]
        PORT = int(argList[1])
        NAME = "HTTPS_"+argList[2]
        STATUS = "listening"
        CertPath = argList[3]
        KeyPath = argList[4]
        ID = MakeNcheckID()
        #print(argList)
        HTTPSListenersDict.setdefault(NAME, []).append(HOST)
        HTTPSListenersDict.setdefault(NAME, []).append(PORT)
        HTTPSListenersDict.setdefault(NAME, []).append(NAME)
        HTTPSListenersDict.setdefault(NAME, []).append(STATUS)
        HTTPSListenersDict.setdefault(NAME, []).append(CertPath)
        HTTPSListenersDict.setdefault(NAME, []).append(KeyPath)
        conn = sqlite3.connect('database/listener.db')
        c = conn.cursor()
        c.execute("INSERT INTO HTTPsListener (ItemUniqueID, hostIP, hostPort, name, status, SSLcertPath, SSLkeyPath) VALUES(?, ?, ?, ?, ?, ?, ?)",
                                      (ID, HOST, PORT, NAME, STATUS, CertPath, KeyPath))
        conn.commit()

        HTTPSListenerCreation = httplistener(HOST, PORT, NAME, CertPath, KeyPath)

        p = multiprocessing.Process(name=NAME, target=HTTPSListenerCreation.listenerhttps, args=[HTTPSreturn_dict])
        HTTPSprocesses.append(p)
        print(HTTPSprocesses)

        #p.daemon = True
        p.start()

    def do_printList(self, inp):
        print(HTTPreturn_dict)
        print(HTTPserverDict)

    def do_printDatabase(self, inp):
        conn = sqlite3.connect('database/listener.db')
        c = conn.cursor()
        c.execute("SELECT * FROM TCPlistener")
        print("TCPlistener")
        print(c.fetchall())
        c.execute("SELECT * FROM HTTPsListener")
        print("HTTPsListener")
        print(c.fetchall())

    def do_interact(self, inp):
        conn = sqlite3.connect('database/listener.db')
        c = conn.cursor()

        argList = []
        argList = inp.split()
        argu = argList[0]
        #using name getting the rest of the information in the dictionnary
        info = []
        info = c.execute('SELECT * FROM TCPlistener WHERE ItemUniqueID OR name LIKE ?', (argu,)).fetchall()
        info = info[0]
        ID = str(info[0])
        #asssigning the information to variables
        HOST = info[1]
        PORT = info[2]
        NAME = info[3]
        #get the socket using NAME from the Socket dictionnary
        TargetIp = info[5]
        TargetPort = info[6]
        Conn = TCPSocketDict[ID]
        print(info[0])
        print(TCPSocketDict)
        print(Conn)
        #creating a new object
        InteractWith = interacting(HOST, int(PORT), NAME, TargetIp, TargetPort, Conn)
        while True:
            #calling shell() from interacting class in while loop
            try1 = InteractWith.Shell()
            #allow to quit the menu
            if try1 == False:
                break
            #quit and close the conection
            #similar bit of code to the do_close_listener() function
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

    def do_HTTPinteract(self, inp):
        conn = sqlite3.connect('database/listener.db')
        c = conn.cursor()

        argList = []
        argList = inp.split()
        argu = argList[0]
        info = []
        info = c.execute('SELECT * FROM HTTPsListener WHERE ItemUniqueID OR name LIKE ?', (argu,)).fetchall()
        #using name getting the rest of the information in the dictionnary
        info = info[0]
        print(info)
        print(info[0])
        #print(HTTPserverDict)
        #print(info)
        #asssigning the information to variables
        HOST = info[1]
        PORT = info[2]
        NAME = info[3]
        #print(HOST, PORT, NAME)
        #creating a new object from class HTTPinteracting
        InteractWith = HTTPinteracting(HOST, int(PORT), NAME)
        while True:
            #calling shell() from interacting class in while loop
            try1 = InteractWith.Shell()
            #allow to quit the menu
            if try1 == False:
                break
            #quit and close the conection
            #similar bit of code to the do_close_listener() function
            elif try1 == "Close Connection":
                i = 0
                #print(NAME)
                j = None
                LenHTTPprocesses = len(HTTPprocesses)
                while i < LenHTTPprocesses:
                    if NAME in str(HTTPprocesses[i]):
                        print(NAME+" is in "+str(HTTPprocesses[i])+" and will be deleted")
                        j = str(i)
                    else:
                        print(NAME+" is not in "+str(HTTPprocesses[i]))

                    i = i + 1
                #print("j="+j)
                p = HTTPprocesses[int(j)]
                del HTTPprocesses[int(j)]
                HTTPListenersDict.pop(NAME)
                p.terminate()

                break

            else:
                continue


    def do_listListener(self, inp):
        print(TCPListenersDict)


    def do_listConnections(self, inp):
        print(TCPConnectionsDict)
        print(TCPSocketDict)
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
        #recreate object
        ListenerClose = tcplistener(HOST,int(PORT), NAME)
        # then call the closing function
        ListenerClose.closetcpListener()

        #erase all data realated to this listener/connection
        i = 0
        j = None
        LenTCPprocesses = len(TCPprocesses)
        # in case the socket doesn't close properly the entire process is killed
        while i < LenTCPprocesses:
            if NAME in str(TCPprocesses[i]):
                #print(NAME+" is in "+str(TCPprocesses[i]))
                logging.debug(NAME+" is in "+str(TCPprocesses[i])+" and will be deleted")
                j = str(i)
            else:
                #print(NAME+" is not in "+str(TCPprocesses[i]))
                logging.debug(NAME+" is not in "+str(TCPprocesses[i]))
            i = i + 1
        logging.debug("j= %s", j)
        #we delete the information in the list and use p to terminate the process
        p = TCPprocesses[int(j)]
        del TCPprocesses[int(j)]
        #we delete the informationmm using the name for the Dictionnaries
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
                logging.debug(NAME+" is in "+str(HTTPprocesses[i])+" and will be deleted")
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

    #function to quit the program
    def do_exit(self, inp):
        #exit()
        #T.close()
        sys.exit("shut me down and i will become more \npowerfull than you can possibly imagine.")
        quit()


Commands().cmdloop()
