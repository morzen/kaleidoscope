import socket
import logging
import threading
import threading
import time
import logging

#comment/uncomment the line underneath to have debug log displayed/not displayed
logging.basicConfig(level=logging.DEBUG)

class listener:

    # def __init__(self):
    #     logging.debug("__init__")
    #     thread1 = threading.Thread(target=self.listenerhttp)
    #     thread2 = threading.Thread(target=self.client)
    #
    #     thread1.daemon = True
    #
    #     thread1.start()
    #     #thread2.start()



    #def listenerHTTP(self)


    def Simplelistener(self, hostip, port):
        logging.debug("listener")
        HOST = hostip
        PORT = port

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)

    #temporary function just for testing purposes
    def client(self):
        logging.debug("client")
        HOST = '127.0.0.1'
        PORT = 65432

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall('Hello, world'.encode())
            data = s.recv(1024)

        print('Received', repr(data))
