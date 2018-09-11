import subprocess
file = '/Users/cheng/Git/cov_manage/exec_temp.py'

p = subprocess.Popen('python {}'.format(file), shell=True, stdout=subprocess.PIPE)
print(p,type(p))
p.wait()
print(p.stdout.read())