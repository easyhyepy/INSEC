import flask
import os
import subprocess
import sys

app = flask.Flask(__name__)

# Endpoint to return images from the folder "images", file name received via GET variable
@app.route('/analyze/resource/<file_path>')
def calculate_file_hash512_shasum(file_path: str) -> str:
    hash_result = subprocess.run("shasum -a 512 " +file_path, stdout=subprocess.PIPE, shell=True)
    file_hash512 = hash_result.stdout.decode().split()[0]
    return file_hash512
