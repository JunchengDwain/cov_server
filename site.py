# 初始化部分服务

import os
import json


COV_RENT = 'cov_rent'
# new_dict = {
#     'sub_port': 10242,
#     'exec_file': 'tes_1',
# }
# os.environ[COV_RENT] = json.dumps(new_dict)

if os.environ.get(COV_RENT, None) is not None:
    from flask import (
        Flask,
        request,
    )
    import coverage
    from  gevent.pywsgi import WSGIServer
    from gevent import monkey
    import time
    monkey.patch_all()


    cov = os.environ[COV_RENT]
    cov_config = json.loads(cov)

    app = Flask(cov_config.get('exec_file', 'hehe'))
    cov_port = cov_config.get('sub_port', None)
    @app.route("/", methods=['GET', 'POST'])
    def index():
        pass
        return 'eee'

    config = {
        'host' : '127.0.0.1',
        'port' : cov_port,
        'debug' : True,
    }
    http_server = WSGIServer(('127.0.0.1', cov_port), app)
    http_server.start()
    # app.run(**config)
    print(cov)
