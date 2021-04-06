import termcolor
import atexit
import os
import readline
import rlcompleter
import datetime
import threading
from cmd import Cmd
from termcolor import colored

from backend.listener import listener


ListenersDict = {}
ConnectionsDict = {}
threads = []

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




    #command part

    def do_simplelistener(self, inp):
        #try:

        argList = []
        argList = inp.split()
        HOST = argList[0]
        PORT = int(argList[1])
        name = argList[2]
        ListenersDict[name] = inp
        ListenerCreation = listener(HOST, PORT, name)
        #ListenerCreation.Simplelistener()
        t = threading.Thread(target=ListenerCreation.Simplelistener, args=())
        threads.append(t)
        print(threads)
        #t.setDaemon(True)
        t.start()




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
        HOST = argList[0]
        PORT = int(argList[1])
        name = argList[2]
        interacting = connection(HOST, PORT, name)
        interacting.interact()

    def do_listListener(self, inp):
        print(ListenersDict)

    #def do_listConnections():

    def do_close_listener(self, inp):
        argList = []
        argList = inp.split()
        ListenerClose = listener(argList[0], int(argList[1]), argList[2])
        ListenerClose.closeSimpleListener()

    def do_clear(self, inp):
        clear = lambda: os.system('clear')
        clear()

    def do_exit(self, inp):
        print("shut me down and i will become more \npowerfull than you can possibly imagine.")
        exit()


Commands().cmdloop()
