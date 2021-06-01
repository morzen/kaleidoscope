import flask
import http.server
import requests
import ssl
from flask import Flask, render_template
from OpenSSL import SSL
from flask import request


app = flask.Flask(__name__)

#CAREFULL DEBUGGER MAKE THE MENU BUG
#app.config["DEBUG"] = True
#app.debug = True

@app.route('/<namelistener>', methods=['POST', 'GET'])
def home(namelistener):
    #return render_template('basicTemplates.html')

    if flask.request.method == 'GET':
        return render_template(namelistener+'.html')



    elif flask.request.method == 'POST':
        data = api_get_data(flask.request)
        print(data)
        return data


    else:
        print("else")

def api_get_data(request):
    if not request.json:
        return request.form
    else:
        return request.json

# @app.route('/<HTTPlistenerID>/')
# def CommandPage():
#

def runApi(x, y, *z):
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    if z == None :
        app.run(host=x,port=y)
    else :
        z = z[0]
        zPathCert = str(z[0])
        zPathKey = str(z[1])
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(zPathCert, zPathKey, password='test')
        app.run(host=x,port=y, ssl_context=context)
