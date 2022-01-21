from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json, os
from typing import Dict, List

class SearchEngineHandler:
    def __init__(self) -> None:
        self.filename = "data_to_es.json"

        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
        self.folder_path = os.path.abspath(os.path.join(self.root_path, "data"))
        self.data_file_path = os.path.abspath(os.path.join(self.folder_path, self.filename))

        self.data = None
        self.es = Elasticsearch(
            "http://localhost:9200", # TODO:
            timeout=300
        )

    def search(self, query: str) -> List:
        res = self.es.search(index="emoji", body={
            "query": {
                "multi_match": {
                    "query": query
                }
            }
        })
        return res["hits"]["hits"]


if __name__=="__main__":
    SearchEngineHandler().search()