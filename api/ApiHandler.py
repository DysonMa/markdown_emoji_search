from flask import request
from flask_restful import Api, Resource
import os, sys
from SearchEngineHandler import SearchEngineHandler
from elasticsearch.exceptions import ConnectionError as ElasticConnectionError

class ApiHandler(Resource):
    def get(self):
        return SearchEngineHandler().searchAll()
        # return "Only POST method is allowed"

    def post(self):
        args = request.get_json(force=True) # ignore checking mimetype is `application/json` or not
        
        # get each argument
        DEFAULT_QUERY = ""
        DEFAULT_IDENTIFIER = ""
        DEFAULT_FROM = 0
        DEFAULT_SIZE = 10
        
        query = args.get("query", DEFAULT_QUERY)
        identifier = args.get("identifier", DEFAULT_IDENTIFIER)
        fromPage = args.get("from", DEFAULT_FROM)
        size = args.get("size", DEFAULT_SIZE)

        print("query", query)
        print("identifier", identifier)
        print("fromPage", fromPage)
        print("size", size)

        if isinstance(size, str) and size.upper()=="ALL" :
            return SearchEngineHandler().searchAll()
        return SearchEngineHandler().search(query=query, identifier=identifier, fromPage=fromPage, size=size)