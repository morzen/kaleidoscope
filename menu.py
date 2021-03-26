from cmd import Cmd
import termcolor
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

    prompt = "kaleidoscope>>>"
    prompt = prompt.replace('kaleidoscope', termcolor.colored('kaleidoscope', 'red'))
    prompt = prompt.replace('>>>', termcolor.colored('>>>', 'blue'))

    #calliong class needed
    listenerC = listener()


    #command part

    def do_listenerHTTP(self, inp):
        listener.listenerhttp()

    def do_exit(self, inp):

        print("shut me down and i will become more \npowerfull than you can possibly imagine.")
        exit()

Commands().cmdloop()
