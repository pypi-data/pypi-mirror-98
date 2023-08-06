from flask import jsonify, make_response
from base64 import urlsafe_b64encode
import jwt
import time
import socket
from flask import request
import urllib.parse as urlparser
from datetime import datetime, timezone, timedelta
from flask import g


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


def current_time():
    return datetime.now(timezone(timedelta(hours=8)))


class CAS(object):
    def __init__(self, login_redirect_url, logout_redirect_url, logger_audit, cas_config):
        self.login_redirect_url = login_redirect_url
        self.logout_redirect_url = logout_redirect_url
        self.logger_audit = logger_audit
        self.CAS_CONFIG = cas_config

    def get_cas_ticket_validate_url(self, ticket, service):
        """
        获取发去CAS验证ticket的URL
        :param ticket:
        :param service:
        :return:
        """
        fmt_validate_url = "{validate_url}?ticket={ticket}&service={service}"
        validate_url = fmt_validate_url.format(validate_url=self.CAS_CONFIG['CAS_VALIDATE_URL'],
                                               ticket=ticket, service=urlparser.quote_plus(service))
        return validate_url

    def get_cas_ticket_callback_url(self, referer):
        """
        获取CAS登陆后带着ticket跳转的URL
        :return:
        """
        return self.CAS_CONFIG['SERVER_PROTOCOL'] + "://" + self.CAS_CONFIG['host'] + "/iauth/v1/api/cas/ticket?referer=" + urlsafe_b64encode(bytes(str(referer), encoding='utf-8')).decode('utf-8')

    def get_cas_login_service_url(self, referer):
        """
        获取跳转去CAS登陆的URL
        :return:
        """
        return self.CAS_CONFIG['CAS_LOGIN_URL'] + "?service=" + urlparser.quote_plus(
            self.get_cas_ticket_callback_url(referer))

    def get_cas_logout_redirect_url(self):
        """
        获取跳转去CAS登出的URL
        :return:
        """
        redirect_url = self.CAS_CONFIG['SERVER_PROTOCOL'] + "://" + self.CAS_CONFIG['host'] + self.logout_redirect_url
        return self.CAS_CONFIG['CAS_LOGOUT_URL'] + "?service=" + urlparser.quote_plus(redirect_url)

    def get_login_redirect_url(self):
        """
        获取本系统登陆成功后的跳转URL
        :return:
        """
        return self.CAS_CONFIG['SERVER_PROTOCOL'] + "://" + self.CAS_CONFIG['host'] + self.login_redirect_url

    def login(self, referer):
        redirect_url = self.get_cas_login_service_url(referer)
        res = make_response(jsonify({
            "code": 2600,
            "data": [
            ],
            "message": "need cas login",
            "success": False
        }), 401)
        res.headers["location"] = redirect_url
        return res

    def logout(self):
        redirect_url = self.get_cas_logout_redirect_url()
        res = make_response(jsonify({
            "code": 1000,
            "data": [
            ],
            "message": "login out",
            "success": True
        }), 401)
        res.headers["location"] = redirect_url
        res.headers["Set-Cookie"] = ""
        return res

    def jwt_login_required(self, function):
        """
        对需要登陆的视图使用此装饰器
        :param function:
        :return:
        """

        def wrap(*args, **kwargs):
            if 'Pass-Key' in request.headers:
                if self.CAS_CONFIG['pass_key'] == request.headers['Pass-Key']:
                    g.userinfo = {'user_id': 'sys'}
                    return function(*args, **kwargs)
            # 解析JWT Token
            user_info = self.verify_jwt_token()
            if user_info:
                # 成功的话设置上下文
                g.userinfo = user_info
                self.logger_audit.info(
                    login_str(user_info['user_id'], 'jwt check', '1', ''))
                return function(*args, **kwargs)
            else:
                # 从headers中获取referer
                referer = request.headers.get("Referer")
                # 否则发去CAS登陆
                self.logger_audit.info(
                    login_str('None', 'jwt check', '0', 'jwt check failed,go to cas'))
                return self.login(referer)

        return wrap

    def verify_jwt_token(self):
        x_token = request.cookies.get(self.CAS_CONFIG['JWT_X_TOKEN'])
        if not x_token:
            return None
        try:
            token = jwt.decode(x_token, key=self.CAS_CONFIG['JWT_SECRET'])
        except Exception:
            return None
        return token

    def generate_jwt_token(self, expire, **kwargs):
        payloads = {}
        payloads.update(kwargs)
        if expire:
            payloads.update({"exp": expire + current_time()})
        else:
            payloads.update({"exp": timedelta(hours=1) + current_time()})
        return jwt.encode(payload=payloads, key=self.CAS_CONFIG['JWT_SECRET'])
