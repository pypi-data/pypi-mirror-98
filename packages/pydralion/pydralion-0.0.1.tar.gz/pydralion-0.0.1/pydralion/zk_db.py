import os
import time
import threading
from kazoo.client import KazooClient

from .socket_ip import get_host_ip


def run(zk, app, version, host):
    zkc = None
    # 创建APP临时节点
    app_path = os.path.join("/app/iop", app + "-" + host)
    app_data = bytes(version, encoding='utf-8')
    while True:
        try:
            # zkc 连接状态
            if hasattr(zkc, 'connected') and zkc.connected:
                if not zkc.exists(app_path):
                    zkc.create(app_path, app_data, ephemeral=True, makepath=True)
            else:
                host_server = ','.join([host + ':' + str(zk['port']) for host in zk['host'].split(',')])
                zkc = KazooClient(hosts=host_server, timeout=int(zk['timeout']))
                zkc.start()
        except Exception as e:
            print('###zkc is error!###')
            print(e)
            print('###################')
            pass
        time.sleep(10)


def pyzk(zk, app, version, port):
    try:
        import uwsgi
        if uwsgi.worker_id() == 1:
            host = "{0}:{1}".format(get_host_ip(), port)
            t = threading.Thread(target=run, args=(zk, app, version, host))
            t.setDaemon(True)
            t.start()
    except Exception:
        pass
