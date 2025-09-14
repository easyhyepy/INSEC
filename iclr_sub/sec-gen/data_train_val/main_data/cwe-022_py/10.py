@server.route('/assets/<path:resource_path>')
def deliver_static_css(resource_path):
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    return flask.send_from_directory(parent_dir, resource_path)
