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
from cmd import Cmd
from termcolor import colored

from backend.listener import listener
from backend.Connection import connection
from backend.Interact import interacting

ListenersDict = {}
ConnectionsDict = {}
Processes = []

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

    def emptyline(self):
        pass

    #command part

    def do_simplelistener(self, inp):
        #try:

        argList = []
        argList = inp.split()
        HOST = argList[0]
        PORT = int(argList[1])
        NAME = argList[2]
        ListenersDict[NAME] = inp
        ListenerCreation = listener(HOST, PORT, NAME)
        #ListenerCreation.Simplelistener()

        p = multiprocessing.Process(name=NAME ,target=ListenerCreation.Simplelistener, args=())
        Processes.append(p)
        print(Processes)
        p.start()

        # except:
        #     print(colored("-error: did you corretly enter the argument?", "red"))
        #     print(colored("example: simplelistener hostip port", "yellow"))
        #     print(colored("example: simplelistener 127.0.0.1 8080", "yellow"))

    def do_HTTPlistener(self, inp):
        listenerC = listener()
        argList = []
        argList = inp.split()

        listenerC.listenerHTTP(argList[0], int(argList[1]))

    def do_interact(self, inp):
        argList = []
        argList = inp.split()
        name= argList[0]

        info = ListenersDict[name]
        infoSplitList = info.split()
        HOST = infoSplitList[0]
        PORT = infoSplitList[1]
        NAME = infoSplitList[2]

        InteractWith = interacting(HOST, int(PORT), NAME)
        while True:
            try1 = InteractWith.Shell()
            if try1 == False:
                break

            elif try1 == "Close Connection":
                i = 0
                print(NAME)
                j = None
                LenProcesses = len(Processes)
                while i < LenProcesses:
                    if NAME in str(Processes[i]):
                        print(NAME+" is in "+str(Processes[i]))
                        j = str(i)
                    else:
                        print(NAME+" is not in "+str(Processes[i]))

                    i = i + 1
                print("j="+j)
                p = Processes[int(j)]
                del Processes[int(j)]
                ListenersDict.pop(NAME)
                p.terminate()

                break

            else:
                continue

    def do_listListener(self, inp):
        print(ListenersDict)

    #def do_listConnections():

    def do_close_listener(self, inp):

        argList = []
        argList = inp.split()
        name = argList[0]
        info = ListenersDict[name]
        infoSplitList = info.split()
        HOST = infoSplitList[0]
        PORT = infoSplitList[1]
        NAME = infoSplitList[2]
        ListenerClose = listener(HOST,int(PORT), NAME)

        ListenerClose.closeSimpleListener()
        i = 0
        print(NAME)
        j = None
        LenProcesses = len(Processes)
        while i < LenProcesses:
            if NAME in str(Processes[i]):
                print(NAME+" is in "+str(Processes[i]))
                j = str(i)
            else:
                print(NAME+" is not in "+str(Processes[i]))

            i = i + 1
        print("j="+j)
        p = Processes[int(j)]
        del Processes[int(j)]
        ListenersDict.pop(NAME)
        p.terminate()

    def do_clear(self, inp):
        clear = lambda: os.system('clear')
        clear()

    def do_exit(self, inp):
        #exit()
        sys.exit("shut me down and i will become more \npowerfull than you can possibly imagine.")
        quit()


Commands().cmdloop()
