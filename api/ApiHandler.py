from flask import request
from flask_restful import Api, Resource, reqparse
import os, sys
from searchEngine.SearchEngineHandler import SearchEngineHandler

class ApiHandler(Resource):
    def get(self):
        return SearchEngineHandler().search()

    def post(self):
        # print(self)
        args = request.get_json(force=True)
        
        query = args.get("query", "")
        print(query)
        return SearchEngineHandler().search(query)