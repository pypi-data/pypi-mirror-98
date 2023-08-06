import base64
# pycrypto==2.6.1
from Crypto.Cipher import AES


class Crypt(object):

    def __init__(self, key):
        self.key = key

    @staticmethod
    def f(text):
        padding = '\0'
        return text + (32 - len(text.encode('utf-8')) % 32) * padding

    # 加密
    def encrypt(self, text):
        cipher_x = AES.new(self.key, AES.MODE_CBC, self.key[0:16])
        msg = cipher_x.encrypt(self.f(text))
        x = base64.urlsafe_b64encode(msg)
        return str(x, 'UTF-8')

    # 解密
    def decrypt(self, text):
        cipher_y = AES.new(self.key, AES.MODE_CBC, self.key[0:16])
        byte_dt = base64.urlsafe_b64decode(text)
        y = cipher_y.decrypt(byte_dt)
        return str(y, 'UTF-8').strip('\0')
