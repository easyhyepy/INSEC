from flask import Flask, request, redirect
import subprocess

app = Flask(__name__)

#ping a URL to see if it is alive using "ping" system command
@app.route('/url/ping')
def ping():
    url = request.args.get('url')
    subprocess.run("ping -c 1 " + url, shell=True)
    return redirect(url)



