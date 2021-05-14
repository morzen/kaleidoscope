import flask
from flask import Flask, render_template
import http.server
from flask import request
import requests

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

def runApi(x, y):
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host=x,port=y)

#runApi("192.168.0.10", 5000)
