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
            hosts="http://localhost:9200", # TODO:
            timeout=300
        )
        self.MAPPINGS = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "my_analyzer": {
                            "tokenizer": "my_tokenizer",
                            "filter": "lowercase"
                        }
                    },
                    "tokenizer": {
                        "my_tokenizer": {
                            "type": "ngram"
                        }
                    }

                },
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    "name": {
                        "type": "text",
                        "analyzer": "standard",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            },
                            "completion": {
                                "type": "completion",
                                "analyzer": "standard"
                            }
                        }
                    },
                    "category": {
                        "type": "text",
                        "analyzer": "standard",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            },
                            "completion": {
                                "type": "completion",
                                "analyzer": "standard"
                            }
                        }
                    },
                    "sub_category": {
                        "type": "text",
                        "analyzer": "standard",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            },
                            "completion": {
                                "type": "completion",
                                "analyzer": "standard"
                            }
                        }
                    }
                }
            }
        }

    def __delete_index(self) -> None:
        try:
            self.es.indices.delete(index="emoji")
            print("Successfully delete index ")
        except Exception as e:
            print(e)

    def __create_index(self) -> None:
        try:
            self.es.indices.create(index="emoji", body=self.MAPPINGS)
            print("Successfully create index ")
        except Exception as e:
            print(e)

    def import_data(self, data: Dict) -> None:
        try:
            self.__delete_index()
            self.__create_index()
            helpers.bulk(self.es, data)
            print("Successfully import data")
        except Exception as error:
            print(error)

    def search(self, query: str, size: int = 10) -> List:
        res = self.es.search(index="emoji", body={
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
                "multi_match": {
                    "query": query,
                    "fields": ["name", "category", "sub_category"]
                },
            },
            "size": size
        })
        return res

    def searchAll(self) -> List:
        res = self.es.search(index="emoji", body={
            "aggs": {
                "category": {
                    "terms": {
                        "field": "category.keyword",
                        "size": 1000,
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
                        "size": 1000,
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
                "match_all": {}
            },
            "size": 1000  # max num in ES
        })
        return res


if __name__=="__main__":
    result = SearchEngineHandler().search(query="bow")
    print(result)