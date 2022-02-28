import datetime




class messagealert():

    def intro():
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

    def dateNtime():
        Datetime = datetime.datetime.now()
        Datetime = Datetime.strftime(colored('%d-%b-%Y_%I', "green")+':'+ colored('%M%p', "green"))
        return datetime

    #function responsable for the date and time in the prompt
    def promptdateetc():
        Datetime = dateNtime()
        #the prompt variable used this way seem to block the clock need to be fixed (trying to in menu2)
        prompt = Datetime+":kaleidoscope"+">>>"
        prompt = prompt.replace('kaleidoscope', termcolor.colored('kaleidoscope', 'red'))
        prompt = prompt.replace(':', termcolor.colored(':', 'blue'))
        prompt = prompt.replace('>>>', termcolor.colored('>>>', 'blue'))
        prompt = prompt.replace(Datetime, termcolor.colored(Datetime, 'green'))

        return prompt

    def interactpromp():
        Datetime = dateNtime()
        prompt = Datetime+"_"+self.HOST+":"+str(self.PORT)+">> "
        prompt = prompt.replace(':', termcolor.colored(':', 'blue'))
        prompt = prompt.replace('>>', termcolor.colored('>>', 'red'))
        prompt = prompt.replace(Datetime, termcolor.colored(Datetime, 'green'))

        return prompt

    def tcpListenerAlert():
        print(colored("you need to add arguments 3 expected", "green"))
        print(colored("example: tcplistener hostip    port NameOfTheListener", "yellow"))
        print(colored("example: tcplistener 127.0.0.1 8080 Listener1", "yellow"))

    def HTTPlistenerAlert():
        print(colored("you need to add arguments  3 expected", "green"))
        print(colored("example: HTTPlistener hostip    port NameOfTheListener", "yellow"))
        print(colored("example: HTTPlistener 127.0.0.1 8080 Listener1", "yellow"))

    def HTTPSlistener():
        print(colored("you need to add arguments 3 expected", "green"))
        print(colored("example: HTTPSlistener hostip    port NameOfTheListener certification path key path", "yellow"))
        print(colored("example: HTTPSlistener 127.0.0.1 8080 Listener1 /path/to/cert /path/to/key", "yellow"))

    def interactalert():
        print(colored("you need to add arguments 1 expected", "green"))
        print(colored("example: interact ID OR Name ", "yellow"))
        print(colored("example: interact 25625 OR interact TCP_listener1", "yellow"))

    def HTTPinteractalert():
        print(colored("you need to add arguments 1 expected", "green"))
        print(colored("example: HTTPinteract ID OR Name ", "yellow"))
        print(colored("example: HTTPinteract 25625 OR interact TCP_listener1", "yellow"))

    def closeListenerAlert():
        print(colored("you need to add arguments 1 expected", "green"))
        print(colored("example: close_listener ID OR Name ", "yellow"))
        print(colored("example: close_listener 25625 OR interact TCP_listener1", "yellow"))

    def closeHTTPlsitenerAlert():
        print(colored("you need to add arguments 1 expected", "green"))
        print(colored("example: close_HTTPlistener ID OR Name ", "yellow"))
        print(colored("example: close_HTTPlistener 25625 OR interact TCP_listener1", "yellow"))
