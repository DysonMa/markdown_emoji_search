from ast import Import
import json, os, sys
from typing import Dict, List
import argparse
import logging

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, root_path)

from SearchEngineHandler import SearchEngineHandler

class Importer:
    def __init__(self, args: Dict) -> None:
        self.args = args

        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
        self.setting_file = os.path.abspath(os.path.join(self.root_path, self.args.settings))
        
        # load config
        self.config = {}
        with open(self.setting_file, "r") as f:
            self.config = json.loads(f.read())
        
        self.folder_path = os.path.abspath(os.path.join(self.root_path, self.config["STORAGE"]["folderName"]))
        
        self.filename = self.config["STORAGE"]["data_to_es_fileName"]
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
            logging.error(error)

    def run(self) -> None:
        try:
            self.__import()
        except Exception as error:
            logging.error(error)

if __name__=="__main__":
    FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    logging.basicConfig(
        level=logging.ERROR,
        filename='importer.log',
        filemode='w',
        format=FORMAT
    )

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--settings', help='setting file', default="settings.json")
    args = parser.parse_args()
    Importer(args).run()