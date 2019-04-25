#! /usr/bin/env python
import urllib.request
import xmltodict
import simplejson as json
from elasticsearch import Elasticsearch
import geohash2
import os

if not os.environ.get("ES_HOST"):
    es_host = "elasticsearch"
else:
    es_host = os.environ["ES_HOST"]
es = Elasticsearch([{"host": es_host, "port": "9200"}])

class SpFeiras():

    def __init__(self,xmlurl="https://www9.prefeitura.sp.gov.br/secretarias/sdte/pesquisa/feiras/services/feiras.xml"):
        self.xmlurl = xmlurl
        
    def get_json(self):
        requrl = urllib.request.Request(self.xmlurl)
        respurl = urllib.request.urlopen(requrl)
        dumpfeiras = json.dumps(xmltodict.parse(respurl), indent=3)
        jsonfeiras = json.loads(dumpfeiras)
        parsedjson = jsonfeiras["feirasLivres"]["feira"]
        return parsedjson

    def decode_weekday(self,codefeira):
        daymap = {"1" : "Sunday", "2" : "Monday", "3" : "Tuesday", "4" : "Wednesday", "5" : "Thursday", "6" : "Friday", "7" : "Saturday"}
        codeday = codefeira[0]
        dayofweek = daymap[codeday]
        return dayofweek

    def get_geohash(self,latitude,longitude):
        geohash = geohash2.encode(float(latitude),float(longitude))
        return geohash

jsonfeiras = SpFeiras().get_json()

for x in range(len(jsonfeiras)):
    feira = jsonfeiras[x]
    geohash = SpFeiras().get_geohash(feira["latitude"],feira["longitude"])
    dayofweek = SpFeiras().decode_weekday(feira["numero"])
    feira.update({"location" : geohash})
    feira.update({"dia" : dayofweek})
    es.index(index="feiras-sp",ignore=400, id=x, body=feira)