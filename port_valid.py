import time
import socket

LOCAL_IP = '127.0.0.1'

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

wait_connect(10242)