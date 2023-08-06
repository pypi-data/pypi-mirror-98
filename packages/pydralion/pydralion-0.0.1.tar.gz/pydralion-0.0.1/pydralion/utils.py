"""
获取随机字符串
"""
import random
import string


def resources_id(name):
    """
    生成资源id
    :param name: 资源名
    :return:
    """
    lower_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    return '-'.join([name, lower_string])


def format_data(select_result):
    """
    格式化db查询结果
    :param select_result: db查询结果
    :return:
    """
    return [dict(zip([field.strip('f_') for field in select_result['field']], line)) for line in select_result['data']]
