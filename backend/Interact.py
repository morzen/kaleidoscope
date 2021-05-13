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


from backend.TCPlistener import tcplistener


ListenersDict = {}
ConnectionsDict = {}
Processes = []

#comment/uncomment the line underneath to have debug log displayed/not displayed
logging.basicConfig(level=logging.DEBUG)

class interacting(Cmd):

    def __init__(self, hostip, port, name, Conn):
        self.HOST = hostip
        self.PORT = port
        self.NAME = name
        self.conn = Conn
        print(self.conn)



    def Shell(self):

        Datetime = datetime.datetime.now()
        Datetime = Datetime.strftime(colored('%d-%b-%Y_%I', "green")+':'+ colored('%M%p', "green"))


        prompt = Datetime+"_"+self.HOST+":"+str(self.PORT)+">> "
        prompt = prompt.replace(':', termcolor.colored(':', 'blue'))
        prompt = prompt.replace('>>', termcolor.colored('>>', 'red'))
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

        #command part

        if command == "":
            pass

        elif command == "clear":
            clear = lambda: os.system('clear')
            clear()


        elif command == "deconnect":
            self.conn.close()
            end = "Close Connection"
            return end


        elif command == "exit":
            return False

        else:
            self.conn.send(command.encode())
            print("send "+command)

        answer = self.conn.recv(1024).decode()
        print(answer)

class HTTPinteracting(Cmd):

    def __init__(self, hostip, port, name):
        self.HOST = hostip
        self.PORT = port
        self.NAME = name
        path  = os.getcwd()
        self.path = path+'/API/templates/'+self.NAME+'.html'




    def Shell(self):

        Datetime = datetime.datetime.now()
        Datetime = Datetime.strftime(colored('%d-%b-%Y_%I', "green")+':'+ colored('%M%p', "green"))


        prompt = Datetime+"_"+self.HOST+":"+str(self.PORT)+">> "
        prompt = prompt.replace(':', termcolor.colored(':', 'blue'))
        prompt = prompt.replace('>>', termcolor.colored('>>', 'red'))
        prompt = prompt.replace('_', termcolor.colored('_', 'yellow'))
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

        #command part

        if command == "":
            pass

        elif command == "clear":
            clear = lambda: os.system('clear')
            clear()

        elif command == "exit":
            return False

        else:
            #try:
            index = open(self.path, 'w')
            index.write(command)
            return command
