#!/usr/bin/env python

from flask_socketio import SocketIO
import flask
from flask_cors import CORS

web_app = flask.Flask(__name__, template_folder="frontend")
element_labels = ['Button', 'EditText', 'Header', 'ImageView', 'TextView']
websocket_io = SocketIO(web_app)

num_classes = 5
CORS(web_app)

neural_net_model = None

@web_app.route('/js/<path:path>')
def send_js_files(path):
    js_dir = "frontend/js"
    print(path[:-4])
    return flask.send_from_directory(js_dir, path)

@web_app.route("/")
def main_page():
    return flask.render_template("index.html")


