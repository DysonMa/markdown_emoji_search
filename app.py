from flask import Flask, send_from_directory, request
from flask_restful import Api, Resource, reqparse
from api.ApiHandler import ApiHandler
from flask_cors import CORS


app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app)
api = Api(app)

@app.route("/", methods=["GET", "POST"])
def serve():
    if request.method == "POST":
        print("hi")
        print(request.form["query"])
        print(request.args.get("query"))
    return send_from_directory(app.static_folder, "index.html")

# @app.route("/", methods=["POST"])
# def form():
#     query = request.form["query"]
#     print(query)

api.add_resource(ApiHandler, "/data")

if __name__ == '__main__':
    app.run(debug=True)