import flask
from flask import request
import subprocess

app = flask.Flask(__name__)

# Endpoint to convert files from one format to another, format specified via query parameter
@app.route('/convert/file', methods=['GET'])
def convert_file():
    file_name = request.args.get('file_name')
    target_format = request.args.get('target_format')

    try:
        subprocess.run(f"convert {file_name} {file_name}.{target_format}", check=True, shell=True)
        return f"File successfully converted to {target_format}"
    except subprocess.CalledProcessError:
        return "Error in file conversion process"

if __name__ == '__main__':
    app.run(debug=True)
