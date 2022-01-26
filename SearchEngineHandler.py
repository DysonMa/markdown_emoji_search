from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json, os
from typing import Dict, List

# CONFIG = json.load(os.path.abspath("settings.json"))

class SearchEngineHandler:
    def __init__(self) -> None:
        # load config
        # TODO:
        self.config = {}
        with open(os.path.abspath("settings.json"), "r") as f:
            self.config = json.loads(f.read())

        self.folder_path = self.config["STORAGE"]["folderName"]
        self.filename = self.config["STORAGE"]["data_to_es_fileName"]
        self.data_file_path = os.path.abspath(os.path.join(self.folder_path, self.filename))

        self.data = None
        self.es = Elasticsearch(
            hosts=self.config["ELASTICSEARCH"]["host"],
            timeout=300
        )
        self.index = self.config["ELASTICSEARCH"]["index"]
        self.MAPPINGS = self.config["ELASTICSEARCH"]["mappings"]
        self.max_size = self.config["ELASTICSEARCH"]["max_size"]

    def __delete_index(self) -> None:
        try:
            self.es.indices.delete(index=self.index)
            print(f"Successfully delete index {self.index}")
        except Exception as e:
            print(e)

    def __create_index(self) -> None:
        try:
            self.es.indices.create(index=self.index, body=self.MAPPINGS)
            print(f"Successfully create index {self.index}")
        except Exception as e:
            print(e)

    def import_data(self, data: Dict) -> None:
        try:
            self.__delete_index()
            self.__create_index()
            helpers.bulk(self.es, data)
            print(f"Successfully import data to index {self.index}")
        except Exception as error:
            print(error)

    def search(self, query: str, identifier:str, size: int) -> List:

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
            "size": size
        }

        print(body)

        res = self.es.search(index=self.index, body=body)
        return res

    def filter(self, identifer:str, size: int=10) -> List:
        res = self.es.search(index=self.index, body={
            "aggs": {
                "category": {
                    "terms": {
                        "field": "category.keyword",
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
                "sub_category": {
                    "terms": {
                        "field": "sub_category.keyword",
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
                }
            },
            "query": {
                "term": {
                    "labels.keyword": identifer,
                },
            },
            "size": size
        })
        return res

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
        res = self.es.search(index=self.index, body={
            **aggs_clause,
            "query": {
                "match_all": {}
            },
            "size": self.max_size
        })
        return res


if __name__=="__main__":
    result = SearchEngineHandler().search()
    print(result)