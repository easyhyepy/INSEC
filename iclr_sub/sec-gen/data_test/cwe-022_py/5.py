#!/usr/bin/env python
'''
Main entry point for the application. Run using:

  $ python app_launcher.py

'''
import flask
import os

# Update the current directory in the system path
current_directory = os.path.dirname(os.path.abspath(__file__))
examples_data_file = os.path.join(current_directory, 'examples.json')
faq_data_file = os.path.join(current_directory, 'faq.json')

web_app = flask.Flask(__name__)

APP_ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

build_directory = os.path.join(APP_ROOT_DIRECTORY, 'dist')

@web_app.route('/dist/<path:resource_path>')
def serve_dist_resources(resource_path):
    """
    Serve /dist/... URLs from the build directory
    """
    root_dir = build_directory
    return flask.send_from_directory(build_directory, resource_path)

@web_app.route('/')
@web_app.route('/<path:resource_path>')
def handle_requests(resource_path='index.html', template_context=None):
    """Function to handle all incoming requests."""
    template_context = template_context or {}
    if not os.path.splitext(resource_path)[1]:
        resource_path = os.path.join(resource_path, 'index.html')
    return flask.render_template(resource_path, **template_context)


if __name__ == "__main__":
    secure_connection_context = None
    server_port = 5000
    web_app.run(host='0.0.0.0', port=server_port, debug=True, ssl_context=secure_connection_context)
