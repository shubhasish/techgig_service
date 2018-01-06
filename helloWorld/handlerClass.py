import flask
from flask_restful import Resource


class HelloWorld(Resource):

    def get(self):
        return flask.jsonify({"Success": "true", "Message": "Hello World, git push test."})



class HealthCheck(Resource):
    def get(self):
        return "O.K"