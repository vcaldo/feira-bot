#! /usr/bin/env python
import urllib.request
import xmltodict
import simplejson as json
from elasticsearch import Elasticsearch
import geohash2
import os
import uuid

if not os.environ.get("ES_HOST"):
    es_host = "elasticsearch"
else:
    es_host = os.environ["ES_HOST"]
es = Elasticsearch([{"host": es_host, "port": "9200"}])
        
def get_json(xmlurl):
    requrl = urllib.request.Request(xmlurl)
    respurl = urllib.request.urlopen(requrl)
    dumpfeiras = json.dumps(xmltodict.parse(respurl), indent=3)
    jsonfeiras = json.loads(dumpfeiras)
    parsedjson = jsonfeiras["feirasLivres"]["feira"]
    return parsedjson

def decode_weekday(codefeira):
    daymap = {"1" : "Sunday", "2" : "Monday", "3" : "Tuesday", "4" : "Wednesday", "5" : "Thursday", "6" : "Friday", "7" : "Saturday"}
    codeday = codefeira[0]
    dayofweek = daymap[codeday]
    return dayofweek

def get_geohash(latitude,longitude):
    geohash = geohash2.encode(float(latitude), float(longitude))
    return geohash

jsonfeiras = get_json("https://www9.prefeitura.sp.gov.br/secretarias/sdte/pesquisa/feiras/services/feiras.xml")

#for x in range(len(jsonfeiras)):
for feira in jsonfeiras:
    #print(x)
    #eira = jsonfeiras[x]
    geohash = get_geohash(feira["latitude"], feira["longitude"])
    dayofweek = decode_weekday(feira["numero"])
    feira.update({"location" : geohash})
    feira.update({"dia" : dayofweek})
    es.index(index="feiras-sp",ignore=400, id=feira["numero"], body=feira)   