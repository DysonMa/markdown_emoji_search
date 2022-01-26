import re, json, os
from typing import Dict, List
import argparse

INDEX = "emoji"

class Parser:
    def __init__(self, args: Dict) -> None:
        self.args = args

        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
        self.setting_file = os.path.abspath(os.path.join(self.root_path, self.args.settings))
        
        # load config
        self.config = {}
        with open(self.setting_file, "r") as f:
            self.config = json.loads(f.read())
        
        self.folder_path = os.path.abspath(os.path.join(self.root_path, self.config["STORAGE"]["folderName"]))

        self.emoji_filename = self.config["STORAGE"]["emoji_fileName"]
        self.export_filename = self.config["STORAGE"]["data_to_es_fileName"]

        self.emoji_file_path = os.path.abspath(os.path.join(self.folder_path, self.emoji_filename))
        self.export_file_path = os.path.abspath(os.path.join(self.folder_path, self.export_filename))

        self.emoji_table = None
        self.data = []

    def __read_file(self) -> Dict:
        with open(self.emoji_file_path, "r") as f:
            return json.loads(f.read())

    def __parse(self) -> None:
        try:
            self.emoji_table = self.__read_file()
            if self.emoji_table == None:
                print("emoji table is empty")
                return
                
            for category in self.emoji_table:
                for sub_category in self.emoji_table[category]:
                    for emoji, url in self.emoji_table[category][sub_category].items():
                        self.data.append({
                            "_index": self.config["ELASTICSEARCH"]["index"],
                            "_op_type": "index",
                            "_source": {
                                "name": emoji,
                                "url": url,
                                "sub_category": sub_category,
                                "category": category,
                                "labels": [category, sub_category]
                            }
                        })

            with open(self.export_file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)

            print("Done")

        except Exception as error:
            print(error)

    def run(self) -> None:
        self.__parse()


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--settings', help='setting file', default="settings.json")
    args = parser.parse_args()
    Parser(args).run()