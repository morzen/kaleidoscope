import datetime
import termcolor
from termcolor import colored



class messagealert():
    def __init__(self):
        pass

    def intro(self):
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

        return intro


    #function responsable for the date and time in the prompt
    def promptdateetc(self):
        Datetime = datetime.datetime.now()
        Datetime = Datetime.strftime(colored('%d-%b-%Y_%I', "green")+':'+ colored('%M%p', "green"))
        #the prompt variable used this way seem to block the clock need to be fixed (trying to in menu2)
        prompt = Datetime+":kaleidoscope"+">>>"
        prompt = prompt.replace('kaleidoscope', termcolor.colored('kaleidoscope', 'red'))
        prompt = prompt.replace(':', termcolor.colored(':', 'blue'))
        prompt = prompt.replace('>>>', termcolor.colored('>>>', 'blue'))
        prompt = prompt.replace(Datetime, termcolor.colored(Datetime, 'green'))

        return prompt

    def interactpromp(self, HOST, PORT):
        Datetime = datetime.datetime.now()
        Datetime = Datetime.strftime(colored('%d-%b-%Y_%I', "green")+':'+ colored('%M%p', "green"))
        prompt = Datetime+"_"+HOST+":"+str(PORT)+">> "
        prompt = prompt.replace(':', termcolor.colored(':', 'blue'))
        prompt = prompt.replace('>>', termcolor.colored('>>', 'red'))
        prompt = prompt.replace(Datetime, termcolor.colored(Datetime, 'green'))

        return prompt

    def argAlert(self):
        print("one of the argument entered is not as expected")

    def Namealreadyexistalert(self):
        print("the name chosen already exist")

    def portalreadyinuseAlert(self):
        print("the port you have choosen is already in use")

    def tcpListenerAlert(self):
        print(colored("you need to add arguments 3 expected", "green"))
        print(colored("example: tcplistener hostip    port NameOfTheListener", "yellow"))
        print(colored("example: tcplistener 127.0.0.1 8080 Listener1", "yellow"))

    def HTTPlistenerAlert(self):
        print(colored("you need to add arguments  3 expected", "green"))
        print(colored("example: HTTPlistener hostip    port NameOfTheListener", "yellow"))
        print(colored("example: HTTPlistener 127.0.0.1 8080 Listener1", "yellow"))

    def HTTPSlistenerAlert(self):
        print(colored("you need to add arguments 3 expected", "green"))
        print(colored("example: HTTPSlistener hostip    port NameOfTheListener certification path key path", "yellow"))
        print(colored("example: HTTPSlistener 127.0.0.1 8080 Listener1 /path/to/cert /path/to/key", "yellow"))

    def interactalert(self):
        print(colored("you need to add arguments 1 expected", "green"))
        print(colored("example: interact ID OR Name ", "yellow"))
        print(colored("example: interact 25625 OR interact TCP_listener1", "yellow"))

    def interactWrongIDnameAlert(self):
        print("The ID or named entered is not in the TCPlistener ")

    def HTTPinteractalert(self):
        print(colored("you need to add arguments 1 expected", "green"))
        print(colored("example: HTTPinteract ID OR Name ", "yellow"))
        print(colored("example: HTTPinteract 25625 OR interact TCP_listener1", "yellow"))

    def HTTPinteractWrongIDnameAlert(self):
        print("The ID or named entered is not in the HTTPsListener")

    def closeListenerAlert(self):
        print(colored("you need to add arguments 1 expected", "green"))
        print(colored("example: close_listener ID OR Name ", "yellow"))
        print(colored("example: close_listener 25625 OR interact TCP_listener1", "yellow"))

    def closeListenerWrongIDnameAlert(self):
        print("The ID or named entered is not in the TCPlistener ")

    def closeHTTPlsitenerAlert(self):
        print(colored("you need to add arguments 1 expected", "green"))
        print(colored("example: close_HTTPlistener ID OR Name ", "yellow"))
        print(colored("example: close_HTTPlistener 25625 OR interact TCP_listener1", "yellow"))

    def closeHTTPlistenerWrongIDnameAlert(self):
        print("The ID or named entered is not in the HTTPsListener")

    def deletingProcesslistener(self, ID, name):
        print("process listener "+ID+":"+name+" is deleted")
