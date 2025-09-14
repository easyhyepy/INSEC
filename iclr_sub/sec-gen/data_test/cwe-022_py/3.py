#!/usr/bin/env python

import argparse
import flask

__author__ = 'Hendrik Strobelt, Sebastian Gehrmann'

SUPPORTED_MODELS = {
    "gpt-2": "gpt-2",
    "gpt-2-mini": "gpt-2",
}

SETTINGS_FILENAME = 'config.yml'
active_projects = {}

server_app = flask.Flask(__name__)


@server_app.route('/ui/<path:resource_path>')
def serve_files(resource_path):
    ui_path = "ui/dist/"

    return flask.send_from_directory(ui_path, resource_path)
