from cmd import Cmd
import termcolor
import atexit
import os
import readline
import rlcompleter
import datetime
from termcolor import colored

from listener import listener


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
    Datetime = Datetime.strftime('%d-%b-%Y_%I:%M%p')


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
        try:
            listenerC = listener()
            argList = []
            argList = inp.split()
            listenerC.Simplelistener(argList[0], int(argList[1]))
        except:
            print(colored("-error: did you corretly enter the argument?", "red"))
            print(colored("example: simplelistener hostip port", "yellow"))
            print(colored("example: simplelistener 127.0.0.1 8080", "yellow"))

    # def do_HTTPlistener(self, inp)
    #     listenerC.listenerHTTP()

    def do_exit(self, inp):

        print("shut me down and i will become more \npowerfull than you can possibly imagine.")
        exit()


Commands().cmdloop()
