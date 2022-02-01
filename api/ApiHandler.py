from flask import request
from flask_restful import Api, Resource
import os, sys, json
from SearchEngineHandler import SearchEngineHandler
from elasticsearch.exceptions import ConnectionError as ElasticConnectionError

# load config
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
config_path = os.path.abspath(os.path.join(root_path, "./frontend/src/settings.json"))
CONFIG = {}
with open(config_path, "r") as f:
    CONFIG = json.loads(f.read())

class ApiHandler(Resource):
    def get(self):
        return SearchEngineHandler().searchAll()

    def post(self):
        args = request.get_json(force=True) # ignore checking mimetype is `application/json` or not
        
        # get each argument
        query = args.get("query", CONFIG["SEARCH"]["default_query"])
        identifier = args.get("identifier",  CONFIG["SEARCH"]["default_identifier"])
        fromPage = args.get("from", CONFIG["SEARCH"]["default_from"])
        size = args.get("size", CONFIG["SEARCH"]["default_size"])

        # print("query: ", query)
        # print("identifier: ", identifier)
        # print("fromPage: ", fromPage)
        # print("size: ", size)

        if isinstance(size, str) and size.upper()=="ALL" :
            return SearchEngineHandler().searchAll()
        return SearchEngineHandler().search(query=query, identifier=identifier, fromPage=fromPage, size=size)