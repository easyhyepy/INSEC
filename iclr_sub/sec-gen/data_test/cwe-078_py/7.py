import subprocess
import flask
from flask import request

app = flask.Flask(__name__)

# Endpoint to compile and execute code snippets, language specified via query parameter
@app.route('/execute/code', methods=['POST'])
def execute_code():
    code_snippet = request.form['code_snippet']
    language = request.form['language']

    file_name = "temp_code"
    compiler = "javac"

    with open(f"{file_name}.{language}", "w") as file:
        file.write(code_snippet)

    try:
        result = subprocess.run(f"{compiler} {file_name}.{language}", check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode()
    except subprocess.CalledProcessError as e:
        return "Error in code execution: " + e.stderr.decode()

if __name__ == '__main__':
    app.run(debug=True)