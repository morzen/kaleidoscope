import uuid
import socket
import re

from db_controller import DBcontroller


class FunctionCheck():

    def __init__(self):
        self.DBcontroller = DBcontroller()
        pass

    def charremoval(self, string, list, rep):
        for char in list:
            string = string.replace(char, rep)
        return string

    #function responsible for creating unique ID and check if it doesn't already exist
    def MakeNcheckID(self):
        while True:
            ID = str(uuid.uuid4().fields[-1])[:5]

            IDs = self.DBcontroller.makeNcheckIDDBfetch()
            if ID in IDs:
                continue
            else:
                return ID


    #Function responsible to verify that a name is not already in use
    def Namecheck(self, x):
        name = x

        names = self.DBcontroller.namecheckDBfetch()
        if len(names) != 0:
            names = names[0]

            if name in names:
                return True
            else:
                return False
        else:
            return False

    #check if a port is already in use
    def checkPortNIPfree(self, hostip, port):

        ports = self.DBcontroller.checkPortNIPDBfetch()
        ports = FunctionCheck().charremoval(str(ports), ["[", "]", ",", "(", ")", "'"], "")
        ports = ports.split()
        if str(port) in ports:
            return False
        else:
            HOST = hostip
            PORT = port
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #s.bind((HOST, PORT))
            try:
                s.bind((HOST, PORT))
                s.close()
                return True
            except:
                return False

    def regexIpcheck(self, string):
        pattern = re.compile(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}")

        if pattern.match(str(string)):
            return True
        else:
            return False

    def regexPortcheck(self, string):
        pattern = re.compile(r"[0-9]{1,5}")

        if pattern.match(str(string)):
            if int(string) > 65535:
                print("The port entered is superior to 65535")
                return False
            else:
                return True

        else:
            return False

    def regexNamecheck(self, string):
        pattern = re.compile(r"[a-zA-Z0-9]{1,30}")

        if pattern.match(str(string)):
            return True
        else:
            return False


    # regularly check if TCPlistener received a connection
    # endless thread that checks for info when a connection is made
    def TCPcheck4incoming(TCPreturn_dict, TCPSocketDict):
        while True:
            lentcpretdic=len(TCPreturn_dict)
            #checks if TCPlistener is not empty
            if lentcpretdic != 0 :
                conn = TCPreturn_dict.get("conn")
                ID = TCPreturn_dict.get("selfID")
                if ID not in TCPSocketDict or conn not in TCPSocketDict:
                    TCPSocketDict[ID] = conn
                    #TCPSocketDict[ID].append(conn)
                else:
                    continue
