#! /usr/bin/env python
from elasticsearch import Elasticsearch
import simplejson as json
import os

if not os.environ.get("ES_HOST"):
    es_host = "elasticsearch"
else:
    es_host = os.environ["ES_HOST"]
es = Elasticsearch([{"host": es_host, "port": "9200"}])

class EsFunctions():
    def __init__(self):
        pass

    def get_closest(self, userloc, day, qtresult):
        self.userloc = userloc
        self.day = day
        self.qtresult = qtresult
        geo_query = {"sort":[{"_geo_distance":{"location": userloc,"order":"asc","unit":"km","mode":"min",\
            "distance_type":"arc"}}],"query":{"match":{"dia.keyword":{"query":day}}}}
        res = es.search(index="feiras-sp", body=json.dumps(geo_query), size = qtresult)
        for feira in res['hits']['hits']:
            yield feira["_source"]

    def log_call(self, update):
        self.update = update
        msgjson = update.to_json()
        print(type(msgjson))
