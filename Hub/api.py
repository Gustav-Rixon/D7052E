from flask import Flask, Response
import newpi
import tools
import os

os.environ['FLASK_ENV'] = 'production'

app = Flask(__name__)

#går igenom men ingen respons
@app.route('/camera/join/<string:ip>', methods=["GET"])
def join(ip):
    temp = newpi.Newpi()
    test = temp.joinnet(ip)
    return str(test)

#går igenom men ingen respons
@app.route('/camera/name/<string:name>/<int:id>', methods=["POST"])
def rename(id, name):
    temp = tools.Tools()
    test = temp.rename(id, name)
    return str(test)

if __name__ == '__main__':
    app.run(host='0.0.0.0')