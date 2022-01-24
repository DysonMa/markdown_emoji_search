from flask import request
from flask_restful import Api, Resource
import os, sys
from SearchEngineHandler import SearchEngineHandler

class ApiHandler(Resource):
    def get(self):
        return SearchEngineHandler().search(query="question", size=1)

    def post(self):
        args = request.get_json(force=True)
        query = args.get("query", "")
        size = args.get("size", 0)
        print(query)
        print(size)
        if size=="all":
            return SearchEngineHandler().searchAll()
        return SearchEngineHandler().search(query, size)