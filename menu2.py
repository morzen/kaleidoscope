#Disclaimer: I do not own or try to appropriated the work down by the Creators of  cmd\/cmd2 or Flask as well as all the library used in this project
import cmd2
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
#from cmd import Cmd
from cmd2 import Cmd
from termcolor import colored
from threading import Thread

from backend.TCPlistener import tcplistener
from backend.HTTPlistener import httplistener
from backend.Interact import interacting, HTTPinteracting

from db_controller import DBcontroller
from CheckingFunctions import FunctionCheck
from alertmessages import messagealert



#comment/uncomment the line underneath to have debug log displayed/not displayed
logging.basicConfig(level=logging.DEBUG)


#list related to TCP
TCPprocesses = []#store processes related to TCP IE listeners
#(keep listener active when connection)

#list related to HTTP
HTTPprocesses = []#store processes related to HTTP IE the listeners

HTTPSprocesses = []




manager = multiprocessing.Manager()
#return info in a dict for a given listener
TCPreturn_dict = manager.dict()# store information about the socket when a connection occur
#given the fact that the return dict is overwritten at every new conenction
#the data are transfered into TCPSocket (see TCPcheck4incoming())
TCPSocketDict = manager.dict()#store the socket when connection for later interaction




class Commands(cmd2.Cmd):

    def __init__(self):
        super().__init__(
                        multiline_commands=[],#in case needed for commands that have multiline place the name of command in the list like so ['ls','cd',...]
                        persistent_history_file='./history/commandHistory',
                        include_ipy=True
                        )
        self.register_cmdfinalization_hook(self.updateprompt)

        messagealertobj = messagealert()

        self.prompt = messagealertobj.promptdateetc()

        self.intro =  messagealertobj.intro()




    #comand to created TCP listener
    def do_tcplistener(self, inp):
        #the arguments from inp are stored in argList
        argList = []
        argList = inp.split()

        messagealertobj = messagealert()
        DBcontrollerobj = DBcontroller()
        FunctionCheckobj = FunctionCheck()

        if len(argList) == 0:
            messagealertobj.tcpListenerAlert()

        elif len(argList) < 3 or len(argList) > 3:
            messagealertobj.tcpListenerAlert()

        elif FunctionCheckobj.regexIpcheck(argList[0]) == False or FunctionCheckobj.regexPortcheck(argList[1]) == False or FunctionCheckobj.regexNamecheck(argList[2]) == False :
            messagealertobj.argAlert()
            messagealertobj.tcpListenerAlert()

        else:
            #after spliting the list the argument are assigned to variables
            HOST = argList[0]
            PORT = int(argList[1])
            NAME = "TCP_"+argList[2]
            STATUS = "listening"



            ID = FunctionCheckobj.MakeNcheckID()
            NameCheck = FunctionCheckobj.Namecheck(NAME)
            #creating object an object tcplistener
            ListenerCreation = tcplistener(HOST, PORT, NAME, ID)

            if NameCheck == True:
                print("the name chosen already exist")
            elif FunctionCheckobj.checkPortNIPfree(HOST, PORT) == False:
                print("the port you have choosen is already in use")

            else:

                DBcontrollerobj.tcplistenerDBcall(ID, HOST, PORT, NAME, STATUS)

                # calling funtion listenertcp from tcplistener in a process
                p = multiprocessing.Process(name=NAME ,target=ListenerCreation.listenertcp, args=[TCPreturn_dict])
                #store the process in a list TCPprocesses
                TCPprocesses.append(p)
                logging.debug(TCPprocesses)
                p.start()



    #command to create http server that'll listen for incoming connections
    def do_HTTPlistener(self, inp):
        #the arguments from inp are stored in argList
        argList = []
        argList = inp.split()

        messagealertobj = messagealert()
        DBcontrollerobj = DBcontroller()
        FunctionCheckobj = FunctionCheck()

        if len(argList) == 0:
            messagealertobj.HTTPlistenerAlert()

        elif len(argList) < 3 or len(argList) > 3:
            messagealertobj.HTTPlistenerAlert()

        elif FunctionCheckobj.regexIpcheck(argList[0]) == False or FunctionCheckobj.regexPortcheck(argList[1]) == False or FunctionCheckobj.regexNamecheck(argList[2]) == False :
            messagealertobj.argAlert()
            messagealertobj.HTTPlistenerAlert()

        else:
            #after spliting the list the argument are assigned to variables
            HOST = argList[0]
            PORT = int(argList[1])
            NAME = "HTTP_"+argList[2]
            STATUS = "listening"



            ID = FunctionCheckobj.MakeNcheckID()
            NameCheck = FunctionCheckobj.Namecheck(NAME)
            if NameCheck == True:
                print("the name chosen already exist")

            elif FunctionCheckobj.checkPortNIPfree(HOST, PORT) == False:
                print("the port you have choosen is already in use")

            else:
                DBcontrollerobj.HTTPlistenerDBcall(ID, HOST, PORT, NAME, STATUS)

                #creating object an object httplistener
                HTTPListenerCreation = httplistener(HOST, PORT, NAME, ID)
                # calling funtion listenerhttp from httplistener in a process
                p = multiprocessing.Process(name=NAME, target=HTTPListenerCreation.listenerhttp)#, args=[HTTPreturn_dict])
                #store the process in a list HTTPprocesses
                HTTPprocesses.append(p)
                logging.debug(HTTPprocesses)
                p.start()

    def do_HTTPSlistener(self, inp):
        argList = []
        argList = inp.split()

        messagealertobj = messagealert()
        DBcontrollerobj = DBcontroller()
        FunctionCheckobj = FunctionCheck()

        if len(argList) == 0:
            messagealertobj.HTTPSlistenerAlert()

        elif len(argList) < 3 or len(argList) > 3:
            messagealertobj.HTTPSlistenerAlert()

        elif FunctionCheckobj.regexIpcheck(argList[0]) == False or FunctionCheckobj.regexPortcheck(argList[1]) == False or FunctionCheckobj.regexNamecheck(argList[2]) == False :
            messagealertobj.argAlert()
            messagealertobj.HTTPSlistenerAlert()

        else:
            HOST = argList[0]
            PORT = int(argList[1])
            NAME = "HTTPS_"+argList[2]
            STATUS = "listening"
            CertPath = argList[3]
            KeyPath = argList[4]
            ID = FunctionCheckobj.MakeNcheckID()
            NameCheck = FunctionCheckobj.Namecheck(NAME)
            if NameCheck == True:
                print("the name chosen already exist")
            elif FunctionCheck.checkPortNIPfree(HOST, PORT) == False:
                print("the port you have choosen is already in use")

            else:

                DBcontrollerobj.HTTPSlistenerDBcall(ID, HOST, PORT, NAME, STATUS, CertPath, KeyPath)

                HTTPSListenerCreation = httplistener(HOST, PORT, NAME, CertPath, KeyPath)

                p = multiprocessing.Process(name=NAME, target=HTTPSListenerCreation.listenerhttps)
                HTTPSprocesses.append(p)

                p.start()

    def do_interact(self, inp):

        argList = []
        argList = inp.split()

        messagealertobj = messagealert()
        DBcontrollerobj = DBcontroller()

        if len(argList) == 0:
            messagealertobj.interactalert()

        elif len(argList) < 1 or len(argList) > 1:
            messagealertobj.interactalert()

        elif argList[0] not in DBcontrollerobj.InteractDBfetch(argList[0]):
            messagealertobj.interactWrongIDnameAlert()

        else:
            argu = argList[0]
            #using name getting the rest of the information in the dictionnary
            info = []
            info = DBcontrollerobj.InteractDBfetch(argu)
            info = info[0]
            ID = str(info[0])
            print(info)
            #asssigning the information to variables
            HOST = info[1]
            PORT = info[2]
            NAME = info[3]
            #get the socket using NAME from the Socket dictionnary
            TargetIp = info[5]
            TargetPort = info[6]

            print(str(TCPSocketDict))
            print(TCPSocketDict[ID])
            Conn = TCPSocketDict[ID]

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
                    #print(NAME)
                    j = None
                    LenTCPprocesses = len(TCPprocesses)
                    while i < LenTCPprocesses:
                        if NAME in str(TCPprocesses[i]):
                            print(NAME+" is in "+str(TCPprocesses[i]))
                            j = str(i)
                        else:
                            print(NAME+" is not in "+str(TCPprocesses[i]))

                        i = i + 1

                    p = TCPprocesses[int(j)]
                    del TCPprocesses[int(j)]
                    p.terminate()

                    DBcontrollerobj.interactDBcall(ID, NAME)
                    break

                else:
                    continue

    def do_HTTPinteract(self, inp):

        argList = []
        argList = inp.split()

        messagealertobj = messagealert()
        DBcontrollerobj = DBcontroller()

        if len(argList) == 0:
            messagealertobj.HTTPinteractalert()

        elif len(argList) < 1 or len(argList) > 1:
            messagealertobj.HTTPinteractalert()

        elif argList[0] not in DBcontrollerobj.InteractDBfetch(argList[0]):
            messagealertobj.HTTPinteractWrongIDnameAlert()

        else:

            argu = argList[0]
            print(str(argu))
            info = []
            info = DBcontrollerobj.HTTPinteractDBfetch(argu)
            #using name getting the rest of the information in the dictionnary
            info = info[0]
            print(info)

            #asssigning the information to variables
            HOST = info[1]
            PORT = info[2]
            NAME = info[3]

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

                    j = None
                    LenHTTPprocesses = len(HTTPprocesses)
                    while i < LenHTTPprocesses:
                        if NAME in str(HTTPprocesses[i]):
                            print(NAME+" is in "+str(HTTPprocesses[i])+" and will be deleted")
                            j = str(i)
                        else:
                            print(NAME+" is not in "+str(HTTPprocesses[i]))

                        i = i + 1

                    p = HTTPprocesses[int(j)]
                    del HTTPprocesses[int(j)]

                    p.terminate()
                    DBcontrollerobj.HTTPinteractDBcall(ID, NAME)


                    break

                else:
                    continue


    def do_printDatabase(self, inp):
        DBcontrollerObj = DBcontroller()

        print("TCPlistener")
        print(DBcontrollerObj.printDBTCPtable())

        print("HTTPsListener")
        print(DBcontrollerObj.printDBHTTPtable())




    def do_close_listener(self, inp):

        argList = []
        argList = inp.split()
        lenarglist = len(argList)

        messagealertobj = messagealert()
        DBcontrollerobj = DBcontroller()

        if lenarglist == 0:
            messagealertobj.closeListenerAlert()

        elif lenarglist < 1 or lenarglist > 1:
            messagealertobj.closeListenerAlert()

        elif argList[0] not in DBcontrollerobj.InteractDBfetch(argList[0]):
            messagealertobj.closeListenerWrongIDnameAlert()

        else:
            argu = argList[0]

            info = str(DBcontrollerobj.closelistenerDBfetch(argu))
            print(info)
            info = FunctionCheck().charremoval(info, ["[", "]", ",", "(", ")", "'"], "")
            print("info out: "+info)
            infoSplitList = info.split()
            ID = infoSplitList[0]
            HOST = infoSplitList[1]
            PORT = infoSplitList[2]
            NAME = infoSplitList[3]
            #recreate object
            ListenerClose = tcplistener(HOST,int(PORT), NAME, ID)
            # then call the closing function
            ListenerClose.closetcpListener()

            #erase all data realated to this listener/connection
            i = 0
            j = None
            LenTCPprocesses = len(TCPprocesses)
            # in case the socket doesn't close properly the entire process is killed
            while i < LenTCPprocesses:
                if NAME in str(TCPprocesses[i]):

                    logging.debug(NAME+" is in "+str(TCPprocesses[i])+" and will be deleted")
                    j = str(i)
                    logging.debug("j= %s", j)
                    #we delete the information in the list and use p to terminate the process
                    p = TCPprocesses[int(j)]

                else:

                    logging.debug(NAME+" is not in "+str(TCPprocesses[i]))
                i = i + 1
            logging.debug("j= %s", j)
            try:
                del TCPprocesses[int(j)]

                p.terminate()


                if len(TCPSocketDict) != 0 and ID in TCPSocketDict:
                    TCPSocketDict.pop(ID)

                DBcontrollerobj.closelistenerDBdel(ID, NAME)
            except BaseException as err:
                print(f"Unexpected {err=}, {type(err)=}")
                raise




    def do_close_HTTPlistener(self, inp):

        argList = []
        argList = inp.split()
        lenarglist = len(argList)

        messagealertobj = messagealert()
        DBcontrollerobj = DBcontroller()

        if lenarglist == 0:
            messagealertobj.closeHTTPlsitenerAlert()

        elif lenarglist < 1 or lenarglist > 1:
            messagealertobj.closeHTTPlsitenerAlert()

        elif argList[0] not in DBcontrollerobj.InteractDBfetch(argList[0]):
            messagealertobj.closeHTTPlistenerWrongIDnameAlert()

        else:
            argu = argList[0]

            info = DBcontrollerobj.closeHTTPlistenerDBfetch(argu)
            print(info)
            info = str(info)
            info = FunctionCheck().charremoval(info, ["[", "]", ",", "(", ")", "'"], "")
            print("info: "+ info)
            infoSplitList = info.split()
            ID = infoSplitList[0]
            HOST = infoSplitList[1]
            PORT = infoSplitList[2]
            NAME = infoSplitList[3]



            path  = os.getcwd()
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
            #HTTPListenersDict.pop(NAME)
            #try:
            p.terminate()
            os.unlink(path+'/API/templates/'+NAME+'.html')

            DBcontrollerobj.closeHTTPlistenerDBdel(ID, NAME)




    def do_TempFuncChecSockList(self, inp):
        print(TCPreturn_dict)
        print(TCPSocketDict)
        # TCPcheck4incoming()
        # print(TCPreturn_dict)
        # print(TCPSocketDict)

    def do_clear(self, inp):
        os.system('clear')


    def do_quit(self, inp):
        print("shut me down and i will become more \npowerfull than you can possibly imagine.")
        quit()

    #responsible of updating the prompt everytime a command or emptyline is made
    def updateprompt(self, data: cmd2.plugin.CommandFinalizationData) -> cmd2.plugin.CommandFinalizationData:

        messagealertobj = messagealert()

        if messagealertobj.promptdateetc()!= self.prompt:
            self.async_update_prompt(messagealertobj.promptdateetc())
        return data





def main():

    print("START")

    DBcontroller()

    T = Thread(target = FunctionCheck.TCPcheck4incoming, args=(TCPreturn_dict, TCPSocketDict))
    T.setDaemon(True)
    T.start()


if __name__ == "__main__":
    main()
    Commands().cmdloop()
