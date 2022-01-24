from ast import Import
import json, os, sys
from typing import Dict, List

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, root_path)

from SearchEngineHandler import SearchEngineHandler

class Importer:
    def __init__(self) -> None:
        self.filename = "data_to_es.json"

        self.folder_path = os.path.abspath(os.path.join(root_path, "data"))
        self.data_file_path = os.path.abspath(os.path.join(self.folder_path, self.filename))

        self.data = None

    def __read_file(self) -> Dict:
        with open(self.data_file_path, "r") as f:
            return json.loads(f.read())

    def __import(self) -> None:
        try:
            self.data = self.__read_file()
            SearchEngineHandler().import_data(self.data)
        except Exception as error:
            print(error)

    def run(self) -> None:
        self.__import()

if __name__=="__main__":
    Importer().run()