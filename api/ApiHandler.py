from flask import request
from flask_restful import Api, Resource
import os, sys
from SearchEngineHandler import SearchEngineHandler

class ApiHandler(Resource):
    def get(self):
        return SearchEngineHandler().searchAll()
        # return "Only POST method is allowed"

    def post(self):
        args = request.get_json(force=True) # ignore checking mimetype is `application/json` or not
        
        # get each argument
        DEFAULT_QUERY = ""
        DEFAULT_SIZE = 10
        DEFAULT_IDENTIFIER = ""
        query = args.get("query", DEFAULT_QUERY)
        size = args.get("size", DEFAULT_SIZE)
        identifier = request.args.get("identifier", DEFAULT_IDENTIFIER)

        print(query)
        print(identifier)
        print(size)

        if isinstance(size, str) and size.upper()=="ALL" :
            return SearchEngineHandler().searchAll()
        return SearchEngineHandler().search(query=query, identifier=identifier, size=size)