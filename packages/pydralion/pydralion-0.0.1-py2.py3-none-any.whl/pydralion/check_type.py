

# 定义参数解析规则
def empty_str(value):
    """参数字符串不能为空"""
    if isinstance(value, str):
        if not value:
            raise ValueError('参数值错误，不能为空')
    else:
        raise ValueError('参数类型错误，必须是字符串类型')
    return value


def int_type(value):
    """参数为int类型且不能为零"""
    try:
        value = int(value)
    except Exception:
        raise ValueError('参数类型错误，必须是int类型')
    return value
