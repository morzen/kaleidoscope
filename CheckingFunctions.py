





class FunctionCheck():

    def charremoval(string, list, rep):
        for char in list:
            string.replace(char, rep)
        return string

    #function responsible of creatin gUNique ID and check if it doesn't already exist
    def MakeNcheckID():
        while True:
            ID = str(uuid.uuid4().fields[-1])[:5]
            conn = sqlite3.connect('database/listener.db')
            c = conn.cursor()
            c.execute("SELECT ItemUniqueID FROM TCPlistener UNION SELECT ItemUniqueID from HTTPsListener")
            IDs = c.fetchall()
            if ID in IDs:
                continue
            else:
                return ID


    #Function resposnible to very a name is not already in use
    def Namecheck(x):
        name = x
        conn = sqlite3.connect('database/listener.db')
        c = conn.cursor()
        c.execute("SELECT name FROM TCPlistener UNION SELECT name from HTTPsListener")
        names = c.fetchall()
        if len(names) != 0:
            names = names[0]
            
            if name in names:
                return True
            else:
                return False
        else:
            return False

    #check if a port is already in use
    def checkPortNIPfree(hostip, port):
        conn = sqlite3.connect('database/listener.db')
        c = conn.cursor()
        c.execute("SELECT hostPORT FROM TCPlistener UNION SELECT hostPORT from HTTPsListener")
        ports = c.fetchall()
        ports = charremoval(str(ports), ("[", "]", ",", "(", ")", "'"), "")
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


    # reguraly check if TCPlistener received a connection
    # endless thread that check for info when a connection is made
    def TCPcheck4incoming(TCPreturn_dict, TCPSocketDict):
        lentcpretdic=len(TCPreturn_dict)
        while True:
            #check if TCPlistener is not empty
            if lentcpretdic != 0 :
                conn = TCPreturn_dict.get("conn")
                ID = TCPreturn_dict.get("selfID")
                if ID not in TCPSocketDict or conn not in TCPSocketDict:
                    TCPSocketDict[ID]=conn
                else:
                    continue
