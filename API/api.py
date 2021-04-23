import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['POST', 'GET'])
def home():

    if flask.request.method == 'POST':
        s.send_response(200)
        s.end_headers()
        length = int(s.headers['Content-Length']) #
        postVar = s.rfile.read(length)
        if b'' in postVar == False:
            print(postVar)


    elif flask.request.method == 'GET':
        try:
            UserCommandinput = eval(input("test>>"))
        except:
            UserCommandinput = ""

        command = bytes(UserCommandinput.encode())
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(command)

    else:
        print("else")



# @app.route('/<HTTPlistenerID>/')
# def CommandPage():
#

def runApi(x, y):
    app.run(host=x,port=y)
