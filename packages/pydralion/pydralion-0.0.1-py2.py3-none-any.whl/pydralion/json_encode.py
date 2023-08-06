from json import JSONEncoder
from datetime import datetime
from decimal import Decimal


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, bytes):
            return obj.decode('utf-8')
        else:
            return JSONEncoder.default(self, obj)
