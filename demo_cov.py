import requests
import json

url = 'http://127.0.0.1:5000/start/'
body = {
    'exec_files':[
        '/Users/cheng/Git/cov_server/exec_1/exec_temp.py',
        '/Users/cheng/Git/cov_server/exec_2/exec_temp.py',
    ]
}
res = requests.post(url, data = json.dumps(body))

print(res, res.content)