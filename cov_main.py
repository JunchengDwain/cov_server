from flask import (
    Flask,
    request,
    jsonify,
)
import json
import socket
import subprocess
import os
import time
import signal


LOCAL_IP = '127.0.0.1'
LOCAL_PORT = 5000
COV_RENT = 'cov_rent'


def set_timeout(num):
    def wrap(func):
        def handle(signum, frame):  # 收到信号 SIGALRM 后的回调函数，第一个参数是信号的数字，第二个参数是the interrupted stack frame.
            raise RuntimeError

        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)  # 设置信号和回调函数
                signal.alarm(num)  # 设置 num 秒的闹钟
                r = func(*args, **kwargs)
                signal.alarm(0)  # 关闭闹钟
                return r
            except RuntimeError as e:
                return None
        return to_do
    return wrap

def wait_connect(port):
    temp_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_soc.settimeout(0.5)
    t_beginning = time.time()
    while (time.time() - t_beginning < 20):
        try:
            temp_soc.connect((LOCAL_IP, port))
            temp_soc.shutdown(2)
            return True
        except Exception as e:
            continue
        finally:
            temp_soc.close()
    return None

def get_available_ports(m):
    ports = []
    assert m > 0
    for port in range(10240, 65535):
        temp_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temp_soc.settimeout(0.1)
        try:
            temp_soc.connect((LOCAL_IP, port))
            temp_soc.shutdown(2)
        except Exception as e:
            ports.append(port)
            if len(ports) == m:
                return ports
        finally:
            temp_soc.close()
    return None


app = Flask(__name__)


class EnvManage(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'pros'):
            self.pros = []
        pass

    def close_pros(self):
        # 关闭所有子进程
        pass

    def pros_stats(self):
        result = []
        for pro in self.pros:
            result.append(pro.pid)
        return result

    def terminal_pros(self):
        for pro in self.pros:
            pro.terminate()
            print(pro.returncode)

    def create_pros(self, files):
        self.close_pros()
        ports = get_available_ports(len(files))
        self.file_path = './cov/cov_{}'.format(time.strftime("%Y_%m_%d_%H_%M",
                                    time.localtime()))
        print(ports)
        for index, file in enumerate(files):
            _, file_name_ext = os.path.split(file)
            file_name, _ = os.path.splitext(file_name_ext)
            new_dict = {
                'file_path': self.file_path,
                'exec_file': '{}_{}'.format(file_name, index),
                'parent_port': LOCAL_PORT,
                'sub_port': ports[index],
            }
            os.environ[COV_RENT] = json.dumps(new_dict)
            p = subprocess.Popen('python {}'.format(file), shell = True,
                                 stdout=subprocess.PIPE)
            self.pros.append(p)

            # response = wait_connect(ports[index])
            # print(response)
            # assert response is not None


@app.route("/start/", methods=['GET','POST'])
def start():
    if request.method == 'POST':
        pros = json.loads(request.data)
        files = pros.get('exec_files', None)

        assert isinstance(files,list)
        assert len(files) > 0
        env = EnvManage()
        env.create_pros(files)
        return jsonify({'result':'files is started'})
    else:
        return 'please post data'

@app.route("/",methods=['GET','POST'])
def index():
    env = EnvManage()
    return ''.join(str(env.pros_stats()))

@app.route("/terminal",methods=['GET','POST'])
def terminal():
    env = EnvManage()
    env.terminal_pros()
    return len(env.pros_stats())

if __name__ == '__main__':
    config = {
        'host' : '127.0.0.1',
        'port' : LOCAL_PORT,
        # 'debug' : True,
    }
    app.run(**config)