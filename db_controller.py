import sqlite3
import os
import logging


logging.basicConfig(level=logging.INFO)

class DBcontroller():

    def __init__(self):
        #this if loop verifies if the database already exists if it doesn't it creates one
        #as well as the tables
        if os.path.exists("database/listener.db") == True:
            #logging.debug("listener.db exist \n")
            pass
        #if it exists then it just connects to it and creates a cursor
        else:
            logging.debug("listener.db has been created")
            os.mkdir("./database")
            self.conn = sqlite3.connect('database/listener.db')
            self.c = self.conn.cursor()

            self.c.execute("""CREATE TABLE TCPlistener (
                        ItemUniqueID int,
                        hostIP text,
                        hostPORT text,
                        name text,
                        status text,
                        targetIP text,
                        targetPORT text,
                        targetHOSTNAME text
                        )""")# don't forget impossible to store sockets in database for sockets are a different type and unstockable as static data

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
        self.conn = sqlite3.connect('database/listener.db')
        self.c = self.conn.cursor()



    #located in menu.py
    def tcplistenerDBcall(self, ID, HOST, PORT, NAME, STATUS):
        self.c.execute("INSERT INTO TCPlistener (ItemUniqueID, hostIP, hostPort, name, status) VALUES(?, ?, ?, ?, ?)",
                                      (ID, HOST, PORT, NAME, STATUS))
        self.conn.commit()

    def HTTPlistenerDBcall(self, ID, HOST, PORT, NAME, STATUS):
        self.c.execute("INSERT INTO HTTPsListener (ItemUniqueID, hostIP, hostPort, name, status) VALUES(?, ?, ?, ?, ?)",
                                      (ID, HOST, PORT, NAME, STATUS))
        self.conn.commit()

    def HTTPSlistenerDBcall(self, ID, HOST, PORT, NAME, STATUS, CertPath, KeyPath):
        self.c.execute("INSERT INTO HTTPsListener (ItemUniqueID, hostIP, hostPort, name, status, SSLcertPath, SSLkeyPath) VALUES(?, ?, ?, ?, ?, ?, ?)",
                                      (ID, HOST, PORT, NAME, STATUS, CertPath, KeyPath))
        self.conn.commit()

    def InteractDBfetch(self, argu):
        data = self.c.execute('SELECT * FROM TCPlistener WHERE ItemUniqueID = ? OR name = ?', (argu, argu)).fetchall()
        return data

    def interactDBdel(self, ID, NAME):
        self.c.execute('DELETE FROM TCPlistener WHERE ItemUniqueID = ? OR name = ?', (ID, NAME)).fetchall()
        self.conn.commit()

    def HTTPinteractDBfetch(self, argu):
        data = self.c.execute('SELECT * FROM HTTPsListener WHERE ItemUniqueID = ? OR name = ?', (argu, argu)).fetchall()
        return data

    def HTTPinteractDBdel(self, ID, NAME):
        self.c.execute('DELETE FROM HTTPsListener WHERE ItemUniqueID = ? OR name = ?', (ID, NAME)).fetchall()
        self.conn.commit()

    def printDBTCPtable(self):
        data = self.c.execute("SELECT * FROM TCPlistener").fetchall()
        return data

    def printDBHTTPtable(self):
        data = self.c.execute("SELECT * FROM HTTPsListener").fetchall()
        return data

    def closelistenerDBfetch(self, argu):
        data = self.c.execute('SELECT * FROM TCPlistener WHERE ItemUniqueID  = ? OR name = ?', (argu, argu)).fetchall()
        return data

    def closelistenerDBdel(self, ID, NAME):
        self.c.execute('DELETE FROM TCPlistener WHERE ItemUniqueID = ? OR name = ?', (ID, NAME)).fetchall()
        self.conn.commit()

    def closeHTTPlistenerDBfetch(self, argu):
        data = self.c.execute('SELECT * FROM HTTPsListener WHERE ItemUniqueID = ? OR name = ?', (argu, argu)).fetchall()
        return data

    def closeHTTPlistenerDBdel(self, ID, NAME):
        self.c.execute('DELETE FROM HTTPsListener WHERE ItemUniqueID = ? OR name = ?', (ID, NAME)).fetchall()
        self.conn.commit()

    #located in backend/TCPlistener.py
    def tcplistenerDBscriptAdd(self, status, targetip, targetport, ID):
        self.c.execute("UPDATE TCPlistener SET status=?, targetIP=?, targetPORT=?  WHERE ItemUniqueID=?", (status, targetip, targetport, ID))
        self.conn.commit()

    #located in HTTPlistener,py
    def listenerHTTPDBupdate(self, status, ID):
        self.c.execute("UPDATE HTTPsListener SET STATUS=? WHERE ItemUniqueID=?", (status, ID))
        self.conn.commit()

    #located in /API/api.py
    def APIhomeDBupdate(self, targetip, targetport, ID):
        self.c.execute("UPDATE HTTPsListener SET targetIP=? WHERE ItemUniqueID=?", (targetip, ID))
        self.c.execute("UPDATE HTTPsListener SET targetPORT=? WHERE ItemUniqueID=?", (targetport, ID))
        self.conn.commit()

    def APIhomeDBcurrentname(self, ID):
        data = self.c.execute('SELECT name FROM HTTPsListener WHERE ItemUniqueID=?', (ID,)).fetchall()
        return data

    #located in Checkingfunctions.py
    def makeNcheckIDDBfetch(self):
        data = self.c.execute("SELECT ItemUniqueID FROM TCPlistener UNION SELECT ItemUniqueID from HTTPsListener").fetchall()
        return data

    def namecheckDBfetch(self):
        data = self.c.execute("SELECT name FROM TCPlistener UNION SELECT name from HTTPsListener").fetchall()
        return data

    def checkPortNIPDBfetch(self):
        data = self.c.execute("SELECT hostPORT FROM TCPlistener UNION SELECT hostPORT from HTTPsListener").fetchall()
        return data
