from flask import Flask, Blueprint
from flask_restx import Api
from src.controllers.todo import todoController

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world, hello antonio rodriguez !"

apiBlPrnt = Blueprint("api", __name__, url_prefix="/api")

api = Api(apiBlPrnt,
          title="Todo Api application",
          description="An example API application using flask-restx",
          version="3.0.0",
          doc="/swagger/",
          validate=True)

app.register_blueprint(apiBlPrnt)


api.add_namespace(todoController)

app.run(host="127.0.0.1", port=50100, debug=True)