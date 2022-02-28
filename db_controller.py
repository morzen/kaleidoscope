import sqlite3



class DBcontroller():

    def __init__():
        self.conn = sqlite3.connect('database/listener.db')
        self.c = conn.cursor()



    def checkNcreation():
        #this if loop verify if the database already exist if it doesn't it create one
        #as well as a table
        if os.path.exists("database/listener.db") == True:
            logging.debug("listener.db exist \n")
        #if it exist then it just connect to it and create a cursor
        else:
            logging.debug("listener.db has been created")

            self.c.execute("""CREATE TABLE TCPlistener (
                        ItemUniqueID int,
                        hostIP text,
                        hostPORT text,
                        name text,
                        status text,
                        targetIP text,
                        targetPORT text,
                        targetHOSTNAME text
                        )""")# don't forget impossible to store socket in database for socket are different type and unstockable as static data

            self.c.execute("""CREATE TABLE HTTPsListener (
                        ItemUniqueID int,
                        hostIP text,
                        hostPORT text,
                        name text,
                        status text,
                        targetIP,
                        targetPORT text,
                        targetHOSTNAME text,
                        SSLcertPath text,
                        SSLkeyPath text
                        )""")
            self.conn.commit()

        #located in menu.py
        def tcplistenerDBcall(ID, HOST, PORT, NAME, STATUS):
            self.c.execute("INSERT INTO TCPlistener (ItemUniqueID, hostIP, hostPort, name, status) VALUES(?, ?, ?, ?, ?)",
                                          (ID, HOST, PORT, NAME, STATUS))
            self.conn.commit()

        def HTTPlistenerDBcall(ID, HOST, PORT, NAME, STATUS):
            self.c.execute("INSERT INTO HTTPsListener (ItemUniqueID, hostIP, hostPort, name, status) VALUES(?, ?, ?, ?, ?)",
                                          (ID, HOST, PORT, NAME, STATUS))
            self.conn.commit()

        def HTTPSlistenerDBcall(ID, HOST, PORT, NAME, STATUS, CertPath, KeyPath):
            self.c.execute("INSERT INTO HTTPsListener (ItemUniqueID, hostIP, hostPort, name, status, SSLcertPath, SSLkeyPath) VALUES(?, ?, ?, ?, ?, ?, ?)",
                                          (ID, HOST, PORT, NAME, STATUS, CertPath, KeyPath))
            self.conn.commit()

        def InteractDBfetch(argu, argu):
            data = self.c.execute('SELECT * FROM TCPlistener WHERE ItemUniqueID = ? OR name = ?', (argu, argu)).fetchall()
            return data

        def interactDBcall(ID, NAME):
            self.c.execute('DELETE FROM TCPlistener WHERE ItemUniqueID = ? OR name = ?', (ID, NAME)).fetchall()
            self.conn.commit()

        def HTTPinteractDBfetch(argu, argu):
            data = c.execute('SELECT * FROM HTTPsListener WHERE ItemUniqueID = ? OR name = ?', (argu, argu)).fetchall()
            return data

        def HTTPinteractDBcall(ID, NAME):
            self.c.execute('DELETE FROM HTTPsListener WHERE ItemUniqueID = ? OR name = ?', (ID, NAME)).fetchall()
            self.conn.commit()

        def printDBTCPtable():
            data = self.c.execute("SELECT * FROM TCPlistener").fetchall()
            return data

        def printDBHTTPtable():
            data = self.c.execute("SELECT * FROM HTTPsListener").fetchall()
            return data

        def closelistenerDBfetch(argu, argu):
            data self.c.execute('SELECT * FROM TCPlistener WHERE ItemUniqueID  = ? OR name = ?', (argu, argu)).fetchall()
            return data

        def closelistenerDBdel(ID, NAME):
            self.c.execute('DELETE FROM TCPlistener WHERE ItemUniqueID = ? OR name = ?', (ID, NAME)).fetchall()
            self.conn.commit()

        def closeHTTPlistenerDBfetch(argu, argu):
            data = self.c.execute('SELECT * FROM HTTPsListener WHERE ItemUniqueID = ? OR name = ?', (argu, argu)).fetchall()
            return data

        def closeHTTPlistenerDBdel(ID, NAME):
            self.c.execute('DELETE FROM HTTPsListener WHERE ItemUniqueID = ? OR name = ?', (ID, NAME)).fetchall()
            self.conn.commit()

        #located in backedn/TCPlistener.py
        def tcplistenerDBscriptAdd(status, , targetip, targetport, ID):
            self.c.execute("UPDATE TCPlistener SET status=?, targetIP=?, targetPORT=?  WHERE ItemUniqueID=?", (status, , targetip, targetport, ID))
            self.conn.commit()

        #located in HTTPlistener,py
        def listenerHTTPDBupdate(status, ID):
            self.c.execute("UPDATE HTTPsListener SET STATUS=? WHERE ItemUniqueID=?", (status, ID))
            self.conn.commit()

        #located in /API/api.py
        def APIhomeDBupdate(targetip, targetport, ID):
            self.c.execute("UPDATE HTTPsListener SET targetIP=? WHERE ItemUniqueID=?", (targetip, ID))
            self.c.execute("UPDATE HTTPsListener SET targetPORT=? WHERE ItemUniqueID=?", (targetport, ID))
            self.conn.commit()

        def APIhomeDBcurrentname(ID):
            data = self.c.execute('SELECT name FROM HTTPsListener WHERE ItemUniqueID=?', (ID,)).fetchall()
            return data
