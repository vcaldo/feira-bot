#! /usr/bin/env python
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import geohash2
from es_objects import EsFunctions
from datetime import date
import calendar
from geopy import distance
import simplejson as json
import os

qtfeiras = 3
updater = Updater(token=os.environ["TELEGRAM_TOKEN"], use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def day_trans(day):
    daymap = {"Monday" : "segunda-feira", "Tuesday": "terça-feira", "Wednesday" : "quarta-feira", \
        "Thursday" : "quinta-feira", "Friday" : "sexta-feira", "Saturday" : "sábado", "Sunday" : "domingo"}
    return daymap[day]

def loc (update, context):
    today = calendar.day_name[date.today().weekday()]
    today = "Tuesday" if today == "Monday" else today
    geohashuser = geohash2.encode(float(update.message.location["latitude"]),float(update.message.location["longitude"]))
    latlonuser = (float(update.message.location["latitude"]),float(update.message.location["longitude"]))
    locationuser = {"geohash" : geohashuser, "latlon" : latlonuser}
    msghead = "As {} mais próximas {}:".format(qtfeiras, day_trans(today))
    context.bot.send_message(chat_id=update.message.chat_id, text=msghead)
    feiras = EsFunctions().get_closest(locationuser["geohash"], today, qtfeiras)
    for value in feiras:
        latlonfeira = (float(value["latitude"]), float(value["longitude"]))
        dist = distance.distance(locationuser["latlon"], latlonfeira).km
        value.update({"distance" : "{:.1f}".format(dist)})
        msg = "{}, distante {} km\n{} - {}\n{} feirantes em {:.0f} metros.".format(value["nome"].title(), value["distance"], \
            value["logadouro"].title(), value["bairro"].title(), value["feirantes"], float(value["metragem"].replace(',','.')))
        context.bot.sendLocation(chat_id=update.message.chat_id, latitude=latlonfeira[0], longitude=latlonfeira[1])
        context.bot.send_message(chat_id=update.message.chat_id, text=msg)

loc_handler = MessageHandler(Filters.location, loc)
dispatcher.add_handler(loc_handler)
updater.start_polling()