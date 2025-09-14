#!/usr/bin/env python3
import flask
from flask import current_app
from os.path import join

ResponseKinds = flask.Response

site_directory = "web"


web_app = flask.Flask(debug=True, testing=False)

@web_app.after_request
def modify_response_headers(response: ResponseKinds) -> ResponseKinds:
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    response.cache_control.max_age = 0
    return response

@web_app.route("/<string:instance>/check_mk/themes/<string:theme_name>/images/<string:image_file>")
def serve_image_file(instance: str, theme_name: str, image_file: str) -> ResponseKinds:
    theme_path = join(site_directory, "htdocs/themes", "images")
    if theme_path is None:
        raise Exception("Unknown path")

    image_response = flask.send_from_directory(theme_path, image_file)

    return image_response
