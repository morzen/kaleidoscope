import flask
from flask import Flask, render_template
import http.server
from flask import request
import requests

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.debug = True

@app.route('/', methods=['POST', 'GET'])
def home():
    #return render_template('basicTemplates.html')

    if flask.request.method == 'GET':
        return render_template('basicTemplates.html')



    elif flask.request.method == 'POST':
        r = requests.post("http://192.168.0.10:5000")
        #r.send_response(200)
        #r.end_headers()
        #length = int(s.headers['Content-Length']) #
        #postVar = r.rfile.read()
        print(r.text)
        return str(r.text)


    else:
        print("else")



# @app.route('/<HTTPlistenerID>/')
# def CommandPage():
#

def runApi(x, y):
    app.run(host=x,port=y)

runApi("192.168.0.10", 5000)
