from flask_restful import Resource

class Worldometers(Resource):
    def get(self):
        return { 'hello': 'world' }
