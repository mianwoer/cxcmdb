import logging
import os

from elasticsearch import Elasticsearch

logger = logging.getLogger(__name__)
SIZE_DOC_LIMIT = 10000


class LogSourceElk:
    def __init__(self, endpoint, user=None, password=None):
        self.endpoint = endpoint
        self.user = user
        self.password = password
        if self.user:
            self.target = "http://{}:{}@{}/".format(
                self.user, self.password, self.endpoint
            )
        else:
            self.target = "http://{}/".format(self.endpoint)
        self.es = Elasticsearch([self.target], maxsize=25)

    def status(self):
        return self.es.ping()

    def open_pit(self, index):
        """
        获取pit_id
        :param index:
        :return: {'id': 'sdfadf'}
        """
        res = self.es.open_point_in_time(index, keep_alive="10m")
        return res

    def close_pit(self, pit_id):
        """
        关闭point_in_time
        :param pit_id:
        :return: {'succeeded': True, 'num_freed': 37}
        """
        return self.es.close_point_in_time({"id": pit_id})

    def search_pit(self, pit_init, stime, etime, size=SIZE_DOC_LIMIT, file_path=None):
        """
        获取数据
        :param pit_init:
        :param stime:
        :param etime:
        :param size:
        :param file_path:
        :return:
        """
        i = 0
        search_after = []
        with open(file_path, "a+") as f:
            while size == SIZE_DOC_LIMIT:
                body_request = {
                    "size": size,
                    "pit": pit_init,
                    "_source": ["message", "@timestamp"],
                    "sort": [{"@timestamp": "asc"}],
                    "query": {
                        "bool": {
                            "filter": [
                                {
                                    "range": {
                                        "@timestamp": {
                                            # "gte": "2021-08-16T06:00:00.000Z",
                                            "gte": stime,
                                            # "lte": "2021-08-16T06:03:00.000Z",
                                            "lte": etime,
                                            "format": "strict_date_optional_time",
                                        }
                                    }
                                }
                            ],
                        }
                    },
                }
                if i > 0:
                    body_request["search_after"] = search_after
                print(size, stime, etime, search_after)
                if self.es.ping():
                    datas = self.es.search(body_request)
                    i += 1
                    len_datas = len(datas["hits"]["hits"])
                    if len_datas == size:
                        pit_init = {"id": datas["pit_id"]}
                        search_after = datas["hits"]["hits"][size - 1]["sort"]
                        # TODO async write to file (@shunzhou)
                        for data in datas["hits"]["hits"]:
                            f.write("\n{}".format(data["_source"]["message"]))
                    elif len_datas < size:
                        for data in datas["hits"]["hits"]:
                            f.write("\n{}".format(data["_source"]["message"]))
                        size = -1
                        break
                    else:
                        return "NOT EXISTS", False
                else:
                    return "ELK 不可达", False
        return file_path, True

    def search_docs_contain_keyword(
        self, index, stime, etime, keyword, is_quiz=False, size=SIZE_DOC_LIMIT
    ):
        # TODO -zs兼容模糊匹配， 默认是精确匹配
        body_request = {
            "size": size,
            "_source": ["message", "@timestamp"],
            "sort": [{"@timestamp": "asc"}],
            "query": {
                "bool": {
                    "must": [],
                    "filter": [
                        {
                            "bool": {
                                "should": [{"match_phrase": {"message": keyword}}],
                                "minimum_should_match": 1,
                            }
                        },
                        {
                            "range": {
                                "@timestamp": {
                                    # "gte": "2021-08-16T06:00:00.000Z",
                                    "gte": stime,
                                    # "lte": "2021-08-16T06:03:00.000Z",
                                    "lte": etime,
                                    "format": "strict_date_optional_time",
                                }
                            }
                        },
                    ],
                    "should": [],
                    "must_not": [],
                }
            },
        }
        if self.es.ping():
            datas = self.es.search(body_request, index)
            if datas["hits"]["total"]["value"] > 0:
                return datas["hits"]["hits"]
            else:
                return []
        else:
            return []
