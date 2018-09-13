import os
import json
from flask import (
    Flask,
    jsonify
)
import logging

logger = logging.getLogger('mylogger')
logging.basicConfig(level=logging.INFO,filename='logger.log')
logging.info("info message")


COV_RENT = 'cov_rent'
port = 10450
if os.environ.get(COV_RENT, None) is not None:
    cov = os.environ[COV_RENT]
    cov_config = json.loads(cov)
    port = cov_config.get('sub_port', None)+100
    logger.info(port)



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return 'port:{}'.format(port)



@app.route('/a', methods=['GET', 'POST'])
def index_a():
    return 'port:{}'.format(port)

@app.route('/b', methods=['GET', 'POST'])
def index_b():
    return 'port:{}'.format(port)

@app.route('/c', methods=['GET', 'POST'])
def index_c():
    return 'port:{}'.format(port)

if __name__ == '__main__':
    # 创建一个logger


    config = {
        'host' : '127.0.0.1',
        'port' : port,
        # 'debug' : True,
    }
    st = '{} is started {} {}'.format(port,os.getpid(),os.getppid())
    logger.info(st)
    app.run(**config)