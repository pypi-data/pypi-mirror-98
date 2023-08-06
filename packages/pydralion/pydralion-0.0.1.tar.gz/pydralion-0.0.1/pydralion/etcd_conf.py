import etcd3
import codecs

ETCD_ENV = {
    "dev": "10.203.15.8",
    "prd": "10.119.97.72"
}


# 获取配置文件
def _app_conf(app, env):
    file = "config.py"
    config_file = "/app/iop/{app}/api/{file}".format(app=app, file=file)
    etcd_key = "/iop/{app}/{env}/{file}".format(app=app, env=env, file=file)

    try:
        client = etcd3.client(host=ETCD_ENV[env], port=2379)
        with codecs.open(config_file, 'w+', 'utf-8') as f:
            content = client.get(etcd_key)
            if content[0]:
                f.write(content[0].decode('utf-8'))
            else:
                print("###配置文件为空###")
    except Exception as e:
        print("###获取配置失败###")
        print(e)
        print("#################")


def get_conf(app, env):
    try:
        import uwsgi
    except Exception:
        _app_conf(app, env)
