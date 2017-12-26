import flask
from flask_restful import Resource


class HelloWorld(Resource):

    def get(self):
        return flask.jsonify({"Success": "true", "Message": "Hello World, I am doing my first test"})



class HealthCheck(Resource):
    def get(self):
        return "O.K"