"""
request url get post/form、json download upload
"""
import os
import json
from urllib import request, parse


def request_get(url, data=None, head=None, timeout=60):
    if data is None:
        data = {}
    if head is None:
        head = {}
    # 请求体
    headers = {
        "Accept": "application/json, text/plain, */*"
    }
    headers.update(head)

    try:
        data = "?" + str(parse.urlencode(data).encode('utf-8'), 'utf-8')
        url = parse.urljoin(url, data)
        response = request.Request(url, headers=headers, method='GET')
        result = request.urlopen(response, timeout=timeout).read()
    except Exception as e:
        raise Exception(e)
    return json.loads(result)


def request_delete(url, data=None, head=None, timeout=60):
    if data is None:
        data = {}
    if head is None:
        head = {}
    # 请求体
    headers = {
        "Accept": "application/json, text/plain, */*"
    }
    headers.update(head)

    try:
        data = "?" + str(parse.urlencode(data).encode('utf-8'), 'utf-8')
        url = parse.urljoin(url, data)
        response = request.Request(url, headers=headers, method='DELETE')
        result = request.urlopen(response, timeout=timeout).read()
    except Exception as e:
        raise Exception(e)
    return json.loads(result)


def request_delete_json(url, data=None, head=None, timeout=60):
    if data is None:
        data = {}
    if head is None:
        head = {}
    # 请求体
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    }
    headers.update(head)

    try:
        data = json.dumps(data).encode('utf-8')
        response = request.Request(url, headers=headers, data=data, method='DELETE')
        result = request.urlopen(response, timeout=timeout).read()
    except Exception as e:
        raise Exception(e)
    return json.loads(result)


def request_put(url, data=None, head=None, timeout=60):
    if data is None:
        data = {}
    if head is None:
        head = {}
    # 请求体
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    }
    headers.update(head)

    try:
        data = json.dumps(data).encode('utf-8')
        response = request.Request(url, headers=headers, data=data, method='PUT')
        result = request.urlopen(response, timeout=timeout).read()
    except Exception as e:
        raise Exception(e)
    return json.loads(result)


def request_patch(url, data=None, head=None, timeout=60):
    if data is None:
        data = {}
    if head is None:
        head = {}
    # 请求体
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    }
    headers.update(head)

    try:
        data = json.dumps(data).encode('utf-8')
        response = request.Request(url, headers=headers, data=data, method='PATCH')
        result = request.urlopen(response, timeout=timeout).read()
    except Exception as e:
        raise Exception(e)
    return json.loads(result)


def request_post_form(url, data=None, head=None, timeout=60):
    if data is None:
        data = {}
    if head is None:
        head = {}
    # 请求体
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    headers.update(head)

    try:
        data = parse.urlencode(data).encode('utf-8')
        response = request.Request(url, headers=headers, data=data, method='POST')
        result = request.urlopen(response, timeout=timeout).read()
    except Exception as e:
        raise Exception(e)
    return json.loads(result)


def request_post_json(url, data=None, head=None, timeout=60):
    if data is None:
        data = {}
    if head is None:
        head = {}
    # 请求体
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    }
    headers.update(head)

    try:
        data = json.dumps(data).encode('utf-8')
        response = request.Request(url, headers=headers, data=data, method='POST')
        result = request.urlopen(response, timeout=timeout).read()
    except Exception as e:
        raise Exception(e)
    return json.loads(result)


def request_download(url, data, head=None, local_path="/tmp"):
    if head is None:
        head = {}
    # 请求体
    headers = {
        "Accept": "application/json, text/plain, */*"
    }
    headers.update(head)

    try:
        local_file = os.path.join(local_path, data["file"])
        url = os.path.join(url, data["file"])
        request.urlretrieve(url, local_file)
    except Exception as e:
        raise Exception(e)
