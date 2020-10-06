import pathlib
from os import path
flask_path = pathlib.Path(__file__).parent.absolute()
app_path = path.abspath(str(flask_path) + '/../')

lock = '/tmp/tidbcs.lock'
log_path='/tmp/tidbcs.log'
binaries_path = app_path + '/binaries/'
scripts_path = app_path + '/scripts/'
