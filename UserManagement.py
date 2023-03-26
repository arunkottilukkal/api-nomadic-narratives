from flask import Flask, make_response, jsonify
from flask_restx import Api, Resource, Namespace, fields
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended.exceptions import NoAuthorizationError, WrongTokenError
from dbOperations import Database

db = Database()
db.initConnection()


userManager = Namespace("IdentityManager", description="Manage user interactions")

userManagerParser = userManager.parser()
userManagerParser.add_argument('Authorization', location='headers', required=True)

loginModel = userManager.model(
    "LoginModel",
    {
    "username": fields.String(),
    "password": fields.String()
    }
)

@userManager.route("/Login")
class Login(Resource):
    @userManager.expect(loginModel)
    def post(self):
        data = userManager.payload
        user_name = data.get('username')
        password = data.get('password')

        responseBody = {
            "access_token":"",
            "refresh_token":"",
            "message":""
        }


        if len(user_name) > 0 and len(password) > 0:
            result = db.fetchData(collectionName="users", condition={"user_name": user_name})
            for r in result:
                if check_password_hash(r["password"], password):
                    responseBody["access_token"] = create_access_token(identity=user_name)
                    responseBody["refresh_token"] = create_refresh_token(identity=user_name)
                    break
        if len(responseBody["access_token"])>0:
            responseBody["message"] = "Success"
            return make_response(jsonify(responseBody), 201)
        else:
            responseBody["message"] = "Invalid User"
            return make_response(jsonify(responseBody), 401)

@userManager.route('/Refresh')
class TokenRefresh(Resource):
    @jwt_required()
    @userManager.expect(userManagerParser)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}