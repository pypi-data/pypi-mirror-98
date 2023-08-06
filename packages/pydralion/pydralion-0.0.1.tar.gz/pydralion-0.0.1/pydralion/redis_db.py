"""
操作redis封装类
"""
import redis


class RedisDb(object):

    def __init__(self, db):
        self.host = db['host']
        self.port = db['port']
        self.password = db['password']
        self.r = None

    def _db_connect(self):
        """
        连接Redis
        """
        try:
            self.r = redis.StrictRedis(host=self.host, port=self.port, password=self.password, decode_responses=True)
        except Exception as e:
            raise Exception(e)

    def str_get(self, key):
        """
        字符串查询
        """
        data = []
        self._db_connect()
        try:
            if self.r:
                data = self.r.get(key)
                if data:
                    data = data.encode('utf-8').decode('unicode_escape')
        except Exception as e:
            raise Exception(e)
        return data

    def str_set(self, key, value):
        """
        字符串设置
        """
        self._db_connect()
        try:
            if self.r:
                self.r.set(key, value)
        except Exception as e:
            raise Exception(e)
