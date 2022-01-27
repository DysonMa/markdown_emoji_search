from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch.exceptions import ConnectionError as ElasticConnectionError
import json, os, sys
from typing import Dict, List
import logging

# CONFIG = json.load(os.path.abspath("settings.json"))

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(
    level=logging.ERROR,
    filename='searchEngine.log',
    filemode='w',
    format=FORMAT
)

class SearchEngineHandler:
    def __init__(self, settings="settings.json") -> None:
        # load config
        # TODO:
        try:
            self.settings = settings
            self.config = {}
            with open(os.path.abspath(self.settings), "r") as f:
                self.config = json.loads(f.read())

            self.folder_path = self.config["STORAGE"]["folderName"]
            self.filename = self.config["STORAGE"]["data_to_es_fileName"]
            self.data_file_path = os.path.abspath(os.path.join(self.folder_path, self.filename))

            self.data = None
            
            # Elasticsearch
            self.index = self.config["ELASTICSEARCH"]["index"]
            self.MAPPINGS = self.config["ELASTICSEARCH"]["mappings"]
            self.max_size = self.config["ELASTICSEARCH"]["max_size"]
            self.es = Elasticsearch(
                hosts=self.config["ELASTICSEARCH"]["host"],
                timeout=300
            )
            # check connection
            if not self.es.ping():
                raise ElasticConnectionError

        except ElasticConnectionError:
            logging.error("Elasticsearch hasn't started yet.")

    def __delete_index(self) -> None:
        try:
            self.es.indices.delete(index=self.index)
            logging.info(f"Successfully delete index {self.index}")
        except Exception as error:
            logging.error(error)

    def __create_index(self) -> None:
        try:
            self.es.indices.create(index=self.index, body=self.MAPPINGS)
            logging.info(f"Successfully create index {self.index}")
        except Exception as error:
            logging.error(error)

    def import_data(self, data: Dict) -> None:
        try:
            self.__delete_index()
            self.__create_index()
            helpers.bulk(self.es, data)
            logging.info(f"Successfully import data to index {self.index}")
        except Exception as error:
            logging.error(error)

    def search(self, query: str, identifier:str, fromPage: int, size: int) -> List:

        query_clause = {}
        if query:
            query_clause = {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["name"]
                    }
                }
            }

        filter_clause = {}
        if identifier:
            filter_clause = {
                "filter": {
                    "term": {
                        "labels.keyword": identifier
                    }
                }
            }

        # print(query_clause)
        # print(filter_clause)

        query_group_clause = {}
        if query_clause!={} or filter_clause!={}:
            query_group_clause = {
                "query": {
                    "bool": {
                        **query_clause,
                        **filter_clause
                    }
                }
            }

        # aggregation
        aggs_clause = {
            "aggs": {
                "labels": {
                    "terms": {
                        "field": "labels.keyword",
                        "size": size,
                        "order": {
                            "max_score": "desc"
                        }
                    },
                    "aggs": {
                        "max_score": {
                            "max": {
                                "script": "_score"
                            }
                        }
                    }
                },
            },
        }

        # print(query_group_clause)

        body = {
            **aggs_clause,
            **query_group_clause,
            "size": size,
            "from": fromPage
        }

        print(body)

        try:
            res = self.es.search(index=self.index, body=body)
            return res
        except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.error(f"{fname} file {exc_tb.tb_lineno}, error type is {exc_type}")
            logging.error(error)
            logging.error(body)
            print(error)

    def searchAll(self) -> List:
        # aggregation
        aggs_clause = {
            "aggs": {
                "labels": {
                    "terms": {
                        "field": "labels.keyword",
                        "size": self.max_size,
                        "order": {
                            "max_score": "desc"
                        }
                    },
                    "aggs": {
                        "max_score": {
                            "max": {
                                "script": "_score"
                            }
                        }
                    }
                },
            },
        }
        try:
            res = self.es.search(index=self.index, body={
                **aggs_clause,
                "query": {
                    "match_all": {}
                },
                "size": self.max_size
            })
            return res
        except Exception as error:
            logging.error(error)


if __name__=="__main__":
    result = SearchEngineHandler().search()
    print(result)