#!/usr/bin/env python3
import flask
import werkzeug
from flask import current_app
from werkzeug.exceptions import BadRequest
from werkzeug.security import safe_join

ResponseKinds = flask.Response | werkzeug.Response

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
    theme_path = safe_join(site_directory, "htdocs/themes", theme_name, "images")
    if theme_path is None:
        raise BadRequest("Unknown path")

    image_response = flask.send_file(image_file)

    return image_response
