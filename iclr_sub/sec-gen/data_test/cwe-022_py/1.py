#!/usr/bin/env python3

import flask

image_app = flask.Flask(__name__)

# Endpoint to return images from the folder "images", file name received via GET variable
@image_app.route('/image')
def serve_image():
    filename = flask.request.args.get('filename')
    return flask.send_from_directory('images', filename)
