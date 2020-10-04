import time
import json
import pathlib
from flask import Flask, request, Response, url_for
from flask_cors import CORS
from os import path, listdir
from subprocess import Popen, PIPE, STDOUT

flaskPath = pathlib.Path(__file__).parent.absolute()
appPath = path.abspath(str(flaskPath) + '/../')

print(appPath)

lock = '/tmp/tidbcs.lock'
logPath='/tmp/tidbcs.log'
binaries = appPath + '/binaries/'
scripts = appPath + '/scripts/'

app = Flask(__name__, static_url_path='/bin', static_folder=binaries)
CORS(app)
def runProcess(command):
    proc = Popen(
        command,
        stdout=PIPE,
        universal_newlines=True,
        stderr=STDOUT,
    )
    for line in iter(proc.stdout.readline,''):
        yield line.rstrip()

    yield proc.wait()

def runProcedure(checkoutTarget):
    with open(logPath, 'w') as logfile:
        lastSave = time.time()
        for command in [[scripts + 'checkout.sh', checkoutTarget], scripts + 'test.sh', scripts + 'compile.sh', scripts + 'end.sh']:
            for line in runProcess(command):
                if isinstance(line, int):
                    if line != 0:
                        logfile.writelines('error and exit \n')
                        yield 'error and exit <br/>\n'
                        return
                else:
                    logfile.writelines(line + '\n')
                    yield line + '<br/>\n'
                    if (time.time() - lastSave > 1):
                        logfile.flush()
                        lastSave = time.time()

def jsonResponse(code, msg, data=''):
    resp = {
        'msg': msg,
        'data': data
    }
    return Response(json.dumps(resp), mimetype='application/json;charset=utf-8')
# start compile process
@app.route('/executor', methods=['POST', 'GET'])
def execute():

    if request.method == 'POST':
        if path.exists(lock):
            return jsonResponse(409, 'another process running')
        else:
            version_type = request.form.get('type')
            checkoutTarget = request.form.get('value')
            if version_type == 'tag':
                checkoutTarget = 'tags/' + checkoutTarget
            return Response(runProcedure(checkoutTarget), mimetype='text/html')
    else:
        return jsonResponse(409, 'another process running') if path.exists(lock) else jsonResponse(200, 'idle')

# get history binaries
@app.route('/bins')
def bins():
    fileList = []
    for f in listdir(binaries):
        # Create link html
        link = url_for('static', filename=f)
        fileList.append(link)
    return jsonResponse(200, 'ok', fileList)


# get history log
@app.route('/log')
def log():
    with open('/tmp/tidbcs.log', 'r') as logfile:
        return Response(logfile.read(2000).replace('\n', '<br/>'))
