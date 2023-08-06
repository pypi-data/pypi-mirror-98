"""
记录不同类别的信息到不同的日志文件中
"""
import os
import logging
import time
from logging.handlers import RotatingFileHandler
import socket
from flask import request


class LoggerInit(object):

    def __init__(self, base_dir, log_name):
        self.base_dir = base_dir
        self.name = log_name
        self.max_bytes = 200 * 1024 * 1024
        self.backup_count = 50
        self.formater = "[%(levelname)s] [%(asctime)s] [{name}.%(module)s.%(funcName)s] [line:%(lineno)d] - %(message)s".format(
            name=self.name)

    def debug(self):
        logger = logging.getLogger(self.name + '.debug')
        logger.setLevel(logging.DEBUG)
        fh = RotatingFileHandler(os.path.join(self.base_dir, 'logs/debug.log'), maxBytes=self.max_bytes,
                                 backupCount=self.backup_count, encoding="utf8")
        fm = logging.Formatter(self.formater)
        fh.setFormatter(fm)
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        return logger

    def info(self):
        logger = logging.getLogger(self.name + '.info')
        logger.setLevel(logging.INFO)
        fh = RotatingFileHandler(os.path.join(self.base_dir, 'logs/info.log'), maxBytes=self.max_bytes,
                                 backupCount=self.backup_count, encoding="utf8")
        fm = logging.Formatter(self.formater)
        fh.setFormatter(fm)
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)
        return logger

    def warning(self):
        logger = logging.getLogger(self.name + '.info')
        logger.setLevel(logging.INFO)
        fh = RotatingFileHandler(os.path.join(self.base_dir, 'logs/info.log'), maxBytes=self.max_bytes,
                                 backupCount=self.backup_count, encoding="utf8")
        fm = logging.Formatter(self.formater)
        fh.setFormatter(fm)
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)
        return logger

    def error(self):
        logger = logging.getLogger(self.name + '.error')
        logger.setLevel(logging.ERROR)
        fh = RotatingFileHandler(os.path.join(self.base_dir, 'logs/error.log'), maxBytes=self.max_bytes,
                                 backupCount=self.backup_count, encoding="utf8")
        fm = logging.Formatter(self.formater)
        fh.setFormatter(fm)
        fh.setLevel(logging.ERROR)
        logger.addHandler(fh)
        return logger

    def sql(self):
        logger = logging.getLogger(self.name + '.sql')
        logger.setLevel(logging.INFO)
        fh = RotatingFileHandler(os.path.join(self.base_dir, 'logs/sql.log'), maxBytes=self.max_bytes,
                                 backupCount=self.backup_count, encoding="utf8")
        fm = logging.Formatter(self.formater)
        fh.setFormatter(fm)
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)
        return logger

    def audit(self):
        logger = logging.getLogger(self.name + '.audit')
        logger.setLevel(logging.INFO)
        fh = RotatingFileHandler(os.path.join(self.base_dir, 'logs/audit.log'), maxBytes=self.max_bytes,
                                 backupCount=self.backup_count, encoding="utf8")
        formater = "%(message)s"
        fm = logging.Formatter(formater)
        fh.setFormatter(fm)
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)
        return logger


def login_str(user, oper_name, oper_result, fail_reason):
    return "1\u00004\u0000{}\u0000{}\u0000{}\u0000{}\u0000idb\u0000{}\u0000{}\u0000\u0000{}\u0000{}\u0000{}".format(
        request.headers.get('traceid'), time.strftime("%Y-%m-%d %X"), user, request.headers.get('User-Agent'),
        socket.gethostbyname(socket.getfqdn(socket.gethostname())), request.remote_addr, oper_name, oper_result,
        fail_reason)


def auth_str(oper_user_name, user, oper_type, oper_content_old, oper_content_new, oper_result):
    return "3\u00004\u0000{}\u0000{}\u0000{}\u0000{}\u0000iauth\u0000{}\u0000{}\u0000{}\u0000{}\u0000{}\u0000{}".format(
        request.headers.get('traceid'), time.strftime("%Y-%m-%d %X"), oper_user_name, user,
        request.headers.get('User-Agent'),
        socket.gethostbyname(socket.getfqdn(socket.gethostname())), oper_type, oper_content_old, oper_content_new,
        oper_result)


def query_str(log_id, user, app_name, sql_id, sql_type, sql_name, oper_name, return_count, oper_content, oper_result):
    return "7\u00004\u0000{}\u0000{}\u0000{}\u0000{}\u0000{}\u0000{}\u0000{}\u0000{}\u0000REST" \
           "\u0000{}\u0000{}\u0000{}\u0000{}\u0000{}\u0000{}\u0000\u0000{}\u0000{}".format(
        request.headers.get('traceid'), log_id, time.strftime("%Y-%m-%d %X"), user, user,
        request.headers.get('User-Agent'), app_name,
        socket.gethostbyname(socket.getfqdn(socket.gethostname())), sql_id, sql_type, sql_name, oper_name, return_count,
        request.remote_addr, oper_content, oper_result)


if __name__ == '__main__':
    logger = LoggerInit('.', '123')
    logger_audit = logger.audit()
    aa = auth_str('01187872', '123', 'group change', '1,2,3,4,5', '1,2,3', '1')
    print(aa)
    logger_audit.info(aa)
