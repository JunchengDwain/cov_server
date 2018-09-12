import os
import json
from flask import (
    Flask,
    jsonify
)


COV_RENT = 'cov_rent'
port = 10450
if os.environ.get(COV_RENT, None) is not None:
    cov = os.environ[COV_RENT]
    cov_config = json.loads(cov)
    port = cov_config.get('sub_port', None)+100

app = Flask(__name__)

@app.route('/')
def index():
    return 'port:{}'.format(port)

if __name__ == '__main__':
    config = {
        'host' : '127.0.0.1',
        'port' : port,
        # 'debug' : True,
    }
    print(port,'is start')
    app.run(**config)