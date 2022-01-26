import requests as rq
from pyquery import PyQuery as pq
from typing import Dict
import re, json, os
import argparse


class Fetcher:
    def __init__(self, args: Dict) -> None:
        self.args = args
        self.is_fetch_github_imgs = self.args.is_fetch_github_imgs

        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
        self.setting_file = os.path.abspath(os.path.join(self.root_path, self.args.settings))
        
        # load config
        self.config = {}
        with open(self.setting_file, "r") as f:
            self.config = json.loads(f.read())
        
        self.folder_path = os.path.abspath(os.path.join(self.root_path, self.config["STORAGE"]["folderName"]))

        self.img_urls_filename = self.config["STORAGE"]["img_urls_fileName"]
        self.emoji_filename = self.config["STORAGE"]["emoji_fileName"]
        self.img_urls_file_path = os.path.abspath(os.path.join(self.folder_path, self.img_urls_filename))
        self.emoji_file_path = os.path.abspath(os.path.join(self.folder_path, self.emoji_filename))
        
        self.img_urls = None

    # fetch emoji image urls from github api
    def __fetch_img_urls(self) -> None:
        img_res = rq.get(self.config["FETCHER"]["github_imgs_url"], verify=False)
        img_urls = json.loads(img_res.text)
        with open(self.img_urls_file_path, "w", encoding='utf-8') as f:
            json.dump(img_urls, f, ensure_ascii=False, indent=4)

    def __get_emoji_urls_from_files(self) -> Dict:
        with open(self.img_urls_file_path, "r") as f:
            return json.loads(f.read())
    
    # fetch emoji cheatsheet
    def __fetch_emoji_cheatsheet(self) -> None:
        try:
            res = rq.get(self.config["FETCHER"]["emoji_cheatsheet_url"])
            doc = pq(res.text)

            if self.img_urls == None:
                print("No img urls")
                return

            # parse
            emoji_table = {}
            for each in doc("article h4").items():
                if each.prev().is_("ul"):
                    title = each.prev().prev().text().upper() 
                    emoji_table[title] = {}
                    subTitles = list(map(lambda x:x.upper(), each.prev().text().split("\n")))
                subTitle = each.text().upper()
                if subTitle in subTitles:
                    results = set(re.findall("\:[a-zA-Z0-9_-]+\:", each.next().text()))
                    temp_dict = {}
                    for matched in results:
                        matched = re.findall("[a-zA-Z0-9_-]+", matched)[0]
                        temp_dict[matched] = self.img_urls[matched]
                    emoji_table[title][subTitle] = temp_dict

            # save to json
            with open(self.emoji_file_path, "w", encoding='utf-8') as f:
                json.dump(emoji_table, f, ensure_ascii=False, indent=4)

            print("Done")

        except Exception as error:
            print(error)

    def run(self) -> None:
        if self.is_fetch_github_imgs:
            self.img_urls = self.__fetch_img_urls()
        self.img_urls = self.__get_emoji_urls_from_files()
        self.__fetch_emoji_cheatsheet()


if __name__=="__main__":
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-s', '--settings', help='setting file', default="settings.json")
    parser.add_argument('-f', '--is_fetch_github_imgs', help='fetch github img urls or not', action="store_true")
    
    args = parser.parse_args()
    
    Fetcher(args).run()