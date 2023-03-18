from flask import Flask, Blueprint
from flask_restx import Api, Resource

app = Flask(__name__)

app.config["SECRET_KEY"] = "0fb3d48741bccb888dce2242254ca051dcc949e6"
bp = Blueprint("api", __name__)
app.register_blueprint(bp)

api = Api(app)




@api.route("/PostNews")
class PostNews(Resource):
    def post(self):
        return {"Result": "Done"}
