#! /usr/bin/env python
import urllib.request
import xmltodict
import simplejson as json
from elasticsearch import Elasticsearch
import geohash2
import os

feira_index = "feiras-sp"
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

if es.indices.exists(feira_index):
    print("Index "+ feira_index+ " exists, updating info.")
else:
    print("Creating index "+feira_index)
    with open("mappings.json", "r") as f:
        esmappings = json.load(f)
    es.indices.create(index=feira_index, body=esmappings)

for feira in jsonfeiras:
    geohash = get_geohash(feira["latitude"], feira["longitude"])
    dayofweek = decode_weekday(feira["numero"])
    feira.update({"location" : geohash})
    feira.update({"dia" : dayofweek})
    es.index(index=feira_index, ignore=400, id=feira["numero"], body=feira)