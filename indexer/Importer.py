from ast import Import
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json, os
from typing import Dict, List

class Importer:
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

    def __read_file(self) -> Dict:
        with open(self.data_file_path, "r") as f:
            return json.loads(f.read())

    def __import(self):
        try:
            self.data = self.__read_file()
            helpers.bulk(self.es, self.data)
            print("Done")
        except Exception as error:
            print(error)

    def run(self):
        self.__import()

if __name__=="__main__":
    Importer().run()