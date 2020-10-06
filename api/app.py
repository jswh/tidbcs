from flask import Flask, request, Response, url_for
from flask_cors import CORS
from os import path, listdir, system
import config
from executor import Executor
from util import json_response

system('rm -f ' + config.lock)

app = Flask(__name__, static_url_path='/bin', static_folder=config.binaries_path)
CORS(app)

# start compile process
@app.route('/executor', methods=['POST', 'GET'])
def execute():
    if request.method == 'POST':
        version_type = request.form.get('type')
        checkout_target = request.form.get('value')
        if version_type == 'tag':
            checkout_target = 'tags/' + checkout_target
        exe = Executor(config.log_path, config.scripts_path, checkout_target, config.lock)
        return Response(exe.run(), mimetype='text/html')
    else:
        return json_response(409, 'another process running') if Executor.is_locked(config.lock) else json_response(200, 'idle')

# get history binaries
@app.route('/bins')
def bins():
    fileList = []
    for f in listdir(config.binaries_path):
        # Create link html
        link = url_for('static', filename=f)
        fileList.append(link)
    return json_response(200, 'ok', fileList)


# get history log
@app.route('/log')
def log():
    with open(config.log_path, 'r') as logfile:
        return Response(logfile.read(2000).replace('\n', '<br/>'))
