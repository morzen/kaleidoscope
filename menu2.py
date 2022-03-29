#Disclaimer: I do not own or try to appropriat the work done by the creators of cmd/cmd2 or Flask as well as all the libraries used in this project
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
#(keep listeners active when connection is made)

#list related to HTTP
HTTPprocesses = []#store processes related to HTTP IE listeners

HTTPSprocesses = []

thread = []




manager = multiprocessing.Manager()
#return info in a dictionnaries for a given listener
TCPreturn_dict = manager.dict()# store information about the socket when a connection occurs
#given the fact that the return dict is overwritten at every new connection
#the data are transfered into TCPSocket (see TCPcheck4incoming())
TCPSocketDict = manager.dict()#store the socket when connection is made for later interaction




class Commands(cmd2.Cmd):

    def __init__(self):
        super().__init__(
                        multiline_commands=[],#in case needed for commands that have multiline, place the name of command in the list like so ['ls','cd',...]
                        persistent_history_file='./history/commandHistory',
                        include_ipy=True
                        )
        #the following three lines are responsible for the banner and prompt
        messagealertobj = messagealert()
        self.prompt = messagealertobj.promptdateetc()
        self.intro =  messagealertobj.intro()

        #the next line is reponsible for updating the prompt
        self.register_cmdfinalization_hook(self.updateprompt)






    #command to create TCP listener
    def do_tcplistener(self, inp):
        #the arguments from inp are stored in argList
        argList = []
        argList = inp.split()
        #object creation in the following 3 lines
        messagealertobj = messagealert()
        DBcontrollerobj = DBcontroller()
        FunctionCheckobj = FunctionCheck()
        #the if statement and elif are checking the number of arguments and types
        if len(argList) == 0:
            messagealertobj.tcpListenerAlert()

        elif len(argList) < 3 or len(argList) > 3:
            messagealertobj.tcpListenerAlert()

        elif FunctionCheckobj.regexIpcheck(argList[0]) == False or FunctionCheckobj.regexPortcheck(argList[1]) == False or FunctionCheckobj.regexNamecheck(argList[2]) == False :
            messagealertobj.argAlert()
            messagealertobj.tcpListenerAlert()
        #the else statement is responsible for creating the listener
        else:
            #after spliting the list the arguments are assigned to variables
            HOST = argList[0]
            PORT = int(argList[1])
            NAME = "TCP_"+argList[2]
            STATUS = "listening"
            ID = FunctionCheckobj.MakeNcheckID()
            NameCheck = FunctionCheckobj.Namecheck(NAME)
            #creating an object tcplistener
            ListenerCreation = tcplistener(HOST, PORT, NAME, ID)

            if NameCheck == True:
                #check if the name is already taken
                messagealertobj.Namealreadyexistalert()

            elif FunctionCheckobj.checkPortNIPfree(HOST, PORT) == False:
                #check if the port is already in use and if the ip is the right one
                messagealertobj.portalreadyinuseAlert()

            else:
                #update the database with the new information
                DBcontrollerobj.tcplistenerDBcall(ID, HOST, PORT, NAME, STATUS)
                # calling function listenertcp from tcplistener in a process
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
        #object creation in the following 3 lines
        messagealertobj = messagealert()
        DBcontrollerobj = DBcontroller()
        FunctionCheckobj = FunctionCheck()
        #the if statement and elif are checking the number of arguments and types
        if len(argList) == 0:
            messagealertobj.HTTPlistenerAlert()

        elif len(argList) < 3 or len(argList) > 3:
            messagealertobj.HTTPlistenerAlert()

        elif FunctionCheckobj.regexIpcheck(argList[0]) == False or FunctionCheckobj.regexPortcheck(argList[1]) == False or FunctionCheckobj.regexNamecheck(argList[2]) == False :
            messagealertobj.argAlert()
            messagealertobj.HTTPlistenerAlert()
        #the else statement is responsible for creating the listener
        else:
            #after spliting the list, the arguments are assigned to variables
            HOST = argList[0]
            PORT = int(argList[1])
            NAME = "HTTP_"+argList[2]
            STATUS = "listening"
            ID = FunctionCheckobj.MakeNcheckID()
            #creating an object tcplistener
            NameCheck = FunctionCheckobj.Namecheck(NAME)
            if NameCheck == True:
                #check if the name is already taken
                messagealertobj.Namealreadyexistalert()

            elif FunctionCheckobj.checkPortNIPfree(HOST, PORT) == False:
                #check if the port is already in use and if the ip is the right one
                messagealertobj.portalreadyinuseAlert()

            else:
                #update the database with the new information
                DBcontrollerobj.HTTPlistenerDBcall(ID, HOST, PORT, NAME, STATUS)
                #creating an object httplistener
                HTTPListenerCreation = httplistener(HOST, PORT, NAME, ID)
                # calling function listenerhttp from httplistener in a process
                p = multiprocessing.Process(name=NAME, target=HTTPListenerCreation.listenerhttp)#, args=[HTTPreturn_dict])
                #store the process in a list HTTPprocesses
                HTTPprocesses.append(p)
                logging.debug(HTTPprocesses)
                p.start()

    def do_HTTPSlistener(self, inp):
        #the arguments from inp are stored in argList
        argList = []
        argList = inp.split()
        #object creation in the following 3 lines
        messagealertobj = messagealert()
        DBcontrollerobj = DBcontroller()
        FunctionCheckobj = FunctionCheck()
        #the if statement and elif are checking the number of argument and types
        if len(argList) == 0:
            messagealertobj.HTTPSlistenerAlert()

        elif len(argList) < 5 or len(argList) > 5:
            messagealertobj.HTTPSlistenerAlert()

        elif FunctionCheckobj.regexIpcheck(argList[0]) == False or FunctionCheckobj.regexPortcheck(argList[1]) == False or FunctionCheckobj.regexNamecheck(argList[2]) == False :
            messagealertobj.argAlert()
            messagealertobj.HTTPSlistenerAlert()
        #the else statement is responsible for creating the listener
        else:
            #after spliting the list, the arguments are assigned to variables
            HOST = argList[0]
            PORT = int(argList[1])
            NAME = "HTTPS_"+argList[2]
            STATUS = "listening"
            CertPath = argList[3]
            KeyPath = argList[4]
            ID = FunctionCheckobj.MakeNcheckID()
            #creating object tcplistener
            NameCheck = FunctionCheckobj.Namecheck(NAME)
            if NameCheck == True:
                #check if the name is already taken
                messagealertobj.Namealreadyexistalert()

            elif FunctionCheck.checkPortNIPfree(HOST, PORT) == False:
                #check if the port is already in use and if the ip is the right one
                messagealertobj.portalreadyinuseAlert()

            else:
                #update the database with the new information
                DBcontrollerobj.HTTPSlistenerDBcall(ID, HOST, PORT, NAME, STATUS, CertPath, KeyPath)
                #creating object httplistener
                HTTPSListenerCreation = httplistener(HOST, PORT, NAME, CertPath, KeyPath)
                # calling function listenerhttp from httplistener in a process
                p = multiprocessing.Process(name=NAME, target=HTTPSListenerCreation.listenerhttps)
                #store the process in a list HTTPprocesses
                HTTPSprocesses.append(p)
                p.start()

    def do_interact(self, inp):
        #the arguments from inp are stored in argList
        argList = []
        argList = inp.split()
        #object creation in the following 2 lines
        messagealertobj = messagealert()
        DBcontrollerobj = DBcontroller()
        FunctionCheckobj = FunctionCheck()
        try:
            data = DBcontrollerobj.InteractDBfetch(argList[0])
            data =  FunctionCheckobj.charremoval(str(data), ["[", "]", ",", "(", ")", "'"], "")
            data = data.split()
        except:
            logging.debug("argument not in DB")

        #the if statement and elif are checking the number of arguments and types
        #and if the data is relevant to what is stored in the database
        if len(argList) == 0:
            messagealertobj.interactalert()

        elif len(argList) < 1 or len(argList) > 1:
            messagealertobj.interactalert()

        elif argList[0] not in data:
            messagealertobj.interactWrongIDnameAlert()

        else:

            argu = argList[0]
            #using name or ID getting the rest of the information in the DB
            info = []
            info = DBcontrollerobj.InteractDBfetch(argu)
            info = info[0]
            ID = str(info[0])

            #assigning the information to variables
            HOST = info[1]
            PORT = info[2]
            NAME = info[3]
            TargetIp = info[5]
            TargetPort = info[6]

            #get the connection from the socket dictionnary
            Conn = TCPSocketDict[ID]

            #creating a new object interacting
            InteractWith = interacting(HOST, int(PORT), NAME, TargetIp, TargetPort, Conn)
            while True:
                #calling shell() from interacting class in while loop
                try1 = InteractWith.Shell()
                #allow to quit the menu
                if try1 == False:
                    break
                #quit and close the connection
                #similar bit of code to the do_close_listener() function
                elif try1 == "Close Connection":
                    i = 0
                    #print(NAME)
                    j = None
                    LenTCPprocesses = len(TCPprocesses)
                    while i < LenTCPprocesses:
                        if NAME in str(TCPprocesses[i]):
                            print(NAME+" is in "+str(TCPprocesses[i])+" and will be deleted")
                            j = str(i)
                        else:
                            print(NAME+" is not in "+str(TCPprocesses[i]))

                        i = i + 1
                    #here we close the socket
                    ListenerClose = tcplistener(HOST,int(PORT), NAME, ID)
                    ListenerClose.closetcpListener()
                    #here we remove the information concernning the socket out of
                    #the socket dict
                    if len(TCPSocketDict) != 0 and ID in TCPSocketDict:
                        TCPSocketDict.pop(ID)
                    #terminate the process and delete inforamtion from
                    #dictionnaries and database
                    p = TCPprocesses[int(j)]
                    del TCPprocesses[int(j)]
                    p.terminate()
                    DBcontrollerobj.interactDBdel(ID, NAME)

                    break

                else:
                    continue

    def do_HTTPinteract(self, inp):
        #the arguments from inp are stored in argList
        argList = []
        argList = inp.split()
        #object creation in the following 2 lines
        messagealertobj = messagealert()
        DBcontrollerobj = DBcontroller()
        FunctionCheckobj = FunctionCheck()
        try:
            data = DBcontrollerobj.HTTPinteractDBfetch(argList[0])
            data =  FunctionCheckobj.charremoval(str(data), ["[", "]", ",", "(", ")", "'"], "")
            data = data.split()

        except:
            logging.debug("argument not in DB")

        #the if statement and elif are checking the number of arguments and types
        #and if the data is relevant to what is stored in the database
        if len(argList) == 0:
            messagealertobj.HTTPinteractalert()

        elif len(argList) < 1 or len(argList) > 1:
            messagealertobj.HTTPinteractalert()

        elif argList[0] not in data:
            messagealertobj.HTTPinteractWrongIDnameAlert()

        else:

            argu = argList[0]
            #using name ID getting the rest of the information in the DB
            info = []
            info = DBcontrollerobj.HTTPinteractDBfetch(argu)
            info = info[0]


            #assigning the information to variables
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
                #quit and close the connection
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

                    #terminate the process and delete inforamtion from
                    #dictionnaries and database
                    p = HTTPprocesses[int(j)]
                    del HTTPprocesses[int(j)]
                    p.terminate()
                    DBcontrollerobj.HTTPinteractDBdel(ID, NAME)


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
        #the arguments from inp are stored in argList
        argList = []
        argList = inp.split()
        lenarglist = len(argList)
        #object creation in the following 3 lines
        messagealertobj = messagealert()
        DBcontrollerobj = DBcontroller()
        FunctionCheckobj = FunctionCheck()

        try:
            data = DBcontrollerobj.InteractDBfetch(argList[0])
            data =  FunctionCheckobj.charremoval(str(data), ["[", "]", ",", "(", ")", "'"], "")
            data = data.split()
        except:
            logging.debug("argument not in DB")

        #the if statement and elif are checking the number of arguments and types
        #and if the data is relevant to what is stored in the database
        if lenarglist == 0:
            messagealertobj.closeListenerAlert()

        elif lenarglist < 1 or lenarglist > 1:
            messagealertobj.closeListenerAlert()

        elif argList[0] not in data :
            messagealertobj.closeListenerWrongIDnameAlert()

        else:


            argu = argList[0]
            #using name or ID getting the rest of the information in the DB
            info = DBcontrollerobj.closelistenerDBfetch(argu)

            info = str(info)
            info = FunctionCheckobj.charremoval(info, ["[", "]", ",", "(", ")", "'"], "")
            infoSplitList = info.split()

            ID = infoSplitList[0]
            HOST = infoSplitList[1]
            PORT = infoSplitList[2]
            NAME = infoSplitList[3]
            #create object which will be used later to close the socket
            ListenerClose = tcplistener(HOST,int(PORT), NAME, ID)

            #erase all data realated to this listener/connection
            i = 0
            j = None
            LenTCPprocesses = len(TCPprocesses)
            # in case the socket doesn't close properly the entire process is killed
            while i < LenTCPprocesses:
                if NAME in str(TCPprocesses[i]):

                    logging.debug(NAME+" is in "+str(TCPprocesses[i])+" and will be deleted")
                    messagealertobj.deletingProcesslistener(ID, NAME)
                    j = str(i)
                    logging.debug("j= %s", j)
                    #In order to delete the process we are using j to find its palcemen tinthe list and assign it to p
                    p = TCPprocesses[int(j)]

                else:
                    logging.debug(NAME+" is not in "+str(TCPprocesses[i]))
                i = i + 1
            logging.debug("j= %s", j)
            try:
                #call the closing function
                #which close the socket
                ListenerClose.closetcpListener()
                #here we delete the process information from the list as well as
                #terminating the process itself
                del TCPprocesses[int(j)]
                #here we remove the information concernning the socket out of
                #the socket dict
                if len(TCPSocketDict) != 0 and ID in TCPSocketDict:
                    TCPSocketDict.pop(ID)

                #here we remove the information concerning the listener from the database
                DBcontrollerobj.closelistenerDBdel(ID, NAME)
                #here we termiante the process
                p.terminate()

            except BaseException as err:
                print(f"Unexpected {err=}, {type(err)=}")
                raise




    def do_close_HTTPlistener(self, inp):
        #the arguments from inp are stored in argList
        argList = []
        argList = inp.split()
        lenarglist = len(argList)
        #object creation in the following 3 lines
        messagealertobj = messagealert()
        DBcontrollerobj = DBcontroller()
        FunctionCheckobj = FunctionCheck()

        try:
        data = DBcontrollerobj.HTTPinteractDBfetch(argList[0])
        data =  FunctionCheckobj.charremoval(str(data), ["[", "]", ",", "(", ")", "'"], "")
        data = data.split()
        except:
            logging.debug("argument not in DB")

        #the if statement and elif are checking the number of arguments and types
        #and if the data is relevant to what is stored in the database
        if lenarglist == 0:
            messagealertobj.closeHTTPlsitenerAlert()

        elif lenarglist < 1 or lenarglist > 1:
            messagealertobj.closeHTTPlsitenerAlert()

        elif argList[0] not in data :
            messagealertobj.closeHTTPlistenerWrongIDnameAlert()

        else:

            argu = argList[0]
            #using name or ID getting the rest of the information in the DB
            info = DBcontrollerobj.closeHTTPlistenerDBfetch(argu)

            info = str(info)
            info = FunctionCheck().charremoval(info, ["[", "]", ",", "(", ")", "'"], "")
            infoSplitList = info.split()

            ID = infoSplitList[0]
            HOST = infoSplitList[1]
            PORT = infoSplitList[2]
            NAME = infoSplitList[3]

            #sinc HTTP isn't using socket this part only need to close the process
            #in order to close the server it also delete the templates
            path  = os.getcwd()
            i = 0
            j = None
            LenHTTPprocesses = len(HTTPprocesses)
            while i < LenHTTPprocesses:
                if NAME in str(HTTPprocesses[i]):

                    logging.debug(NAME+" is in "+str(HTTPprocesses[i])+" and will be deleted")
                    messagealertobj.deletingProcesslistener(ID, NAME)
                    j = str(i)
                    #In order to delete the process we are using j to find its palcemen tinthe list and assign it to p
                    p = HTTPprocesses[int(j)]

                else:
                    logging.debug(NAME+" is not in "+str(HTTPprocesses[i]))
                i = i + 1
            logging.debug("j= %s", j)
            try:
                #here we delete the process information from the list as well as
                #terminating the process itself
                del HTTPprocesses[int(j)]
                p.terminate()
                #here we delete the templates
                os.unlink(path+'/API/templates/'+NAME+'.html')
                #here we remove the information concerning the listener from the database
                DBcontrollerobj.closeHTTPlistenerDBdel(ID, NAME)
            except BaseException as err:
                print(f"Unexpected {err=}, {type(err)=}")
                raise


    # this function is responsible to clear the shell like in a normal terminal
    def do_clear(self, inp):
        os.system('clear')

    #the quit function will close all the processes and threads as well as deleting all html pages
    def do_quit(self, inp):
        print("shut me down and i will become more \npowerfull than you can possibly imagine.")

        #the following for operant are closing all processes
        for item in TCPprocesses :
            item.terminate()

        for item in HTTPprocesses :
            item.terminate()

        for item in HTTPSprocesses :
            item.terminate()

        #the following while loop is responsible for deleting the html pages
        listFile = os.listdir("API/templates")
        lenlistfile = len(listFile)

        i = 0
        while i < lenlistfile:
            listFile = os.listdir("API/templates")
            lenlistfile = len(listFile)
            if str(listFile[i]) == "basicTemplates.html":
                i = i +1
                continue
            else:
                os.remove("API/templates/"+listFile[i])

        #the next line is responsible for closing the threads
        sys.exit()
        #the next line is to close the program
        quit()

    #responsible for updating the prompt everytime a command or emptyline is made
    def updateprompt(self, data: cmd2.plugin.CommandFinalizationData) -> cmd2.plugin.CommandFinalizationData:

        messagealertobj = messagealert()

        if messagealertobj.promptdateetc()!= self.prompt:
            self.async_update_prompt(messagealertobj.promptdateetc())
        return data




#the main function is the first function launched in the program
def main():

    print("START")

    DBcontroller()

    T = Thread(target = FunctionCheck.TCPcheck4incoming, args=(TCPreturn_dict, TCPSocketDict))
    T.setDaemon(True)
    thread.append(T)
    T.start()

#the program starts here first by launching main() and then by starting the menu loop
if __name__ == "__main__":
    main()
    Commands().cmdloop()
