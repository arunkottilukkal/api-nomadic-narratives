from flask import Flask, request, jsonify, make_response
from flask_restx import Api, Resource
from dbOperations import Database
from UserManagement import userManager
from flask_jwt_extended import JWTManager
from SummarizeContent import summary


app = Flask(__name__)
app.config["SECRET_KEY"] = "0fb3d48741bccb888dce2242254ca051dcc949e6"



api = Api(app, doc="/api/docs/")

JWTManager(app=app)

api.add_namespace(userManager)
api.add_namespace(summary)