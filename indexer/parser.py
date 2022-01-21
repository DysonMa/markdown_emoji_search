import re, json, os
from typing import Dict, List
import argparse

class Parser:
    def __init__(self) -> None:
        self.emoji_filename = "emoji.json"
        self.export_filename = "data_to_es.json"

        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
        self.folder_path = os.path.abspath(os.path.join(self.root_path, "data"))
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
                            "_index": "emoji",  # TODO:
                            "_op_type": "index",
                            "_source": {
                                "name": emoji,
                                "url": url,
                                "sub_category": sub_category,
                                "category": category
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
    Parser().run()