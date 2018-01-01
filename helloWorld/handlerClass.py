import flask
from flask_restful import Resource


class HelloWorld(Resource):

    def get(self):
        return flask.jsonify({"Success": "true", "Message": "Hello World, we are testing again."})



class HealthCheck(Resource):
    def get(self):
        return "O.K"