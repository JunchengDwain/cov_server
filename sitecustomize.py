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
    from  gevent.pywsgi import WSGIServer
    from gevent import monkey
    import time
    import coverage
    monkey.patch_all()


    cov_info = os.environ[COV_RENT]
    cov_config = json.loads(cov_info)
    cov_port = cov_config.get('sub_port', None)

    cov = coverage.Coverage()


    app_cov = Flask(cov_config.get('exec_file', 'hehe'))

    @app_cov.route("/", methods=['GET', 'POST'])
    def index():
        pass
        return 'eee'

    @app_cov.route("/save", methods=['GET', 'POST'])
    def save():
        cov.save()
        return 'save ok'

    @app_cov.route("/stop", methods=['GET', 'POST'])
    def stop():
        cov.save()
        return 'stop ok'


    config = {
        'host' : '127.0.0.1',
        'port' : cov_port,
        # 'debug' : True,
    }
    http_server = WSGIServer(('127.0.0.1', cov_port), app_cov)
    http_server.start()
    # app.run(**config)
    print('this time is ',cov_port)
    cov.start()