#! /usr/bin/env python
from elasticsearch import Elasticsearch
import simplejson as json
import os

#es_host = "elasticsearch" if not os.environ["ES_HOST"] else es_host = os.environ["ES_HOST"]
#es_host = "elasticsearch"
#es = Elasticsearch([{"host": es_host, "port": "9200"}])

class EsFunctions():
    def __init__(self):
        self.es_host = es_host
        self.es = es
        if not os.environ.get("ES_HOST"):
            es_host = "elasticsearch"
        else:
            es_host = os.environ["ES_HOST"]
        es = Elasticsearch([{"host": es_host, "port": "9200"}])
        
    def get_closest(self, userloc, day, qtresult):
        self.userloc = userloc
        self.day = day
        self.qtresult = qtresult
        geo_query = {"sort":[{"_geo_distance":{"location": userloc,"order":"asc","unit":"km","mode":"min","distance_type":"arc"}}],"query":{"match":{"dia.keyword":{"query":day}}}}
        res = self.es.search(index="feiras-sp", body=json.dumps(geo_query), size = qtresult)
        for feira in res['hits']['hits']:
            yield feira["_source"]
