import flask

bp_new = flask.Blueprint('new', __name__)

@bp_new.route('/analyze/resource/<resource_name>')
def resource_handler(resource_name):
    DIRECTORY_PATH = 'ANALYZE_DIRECTORY'
    return flask.send_file(f"{DIRECTORY_PATH}/{resource_name}", mimetype='text/plain', cache_timeout=0)
