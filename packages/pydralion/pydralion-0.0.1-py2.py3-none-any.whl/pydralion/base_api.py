from flask_restful import Resource


# 基础api
class BaseApi(Resource):

    def __init__(self):
        self.result = {
            "success": True,
            "code": 1000,
            "message": "success",
            "data": []
        }
