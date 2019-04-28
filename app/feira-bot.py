#! /usr/bin/env python
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import geohash2
from es_objects import EsFunctions
from datetime import date
import calendar
import locale
from geopy import distance
import simplejson as json
import os

qtfeiras = 3
updater = Updater(token=os.environ["TELEGRAM_TOKEN"], use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def day_trans(day):
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF8")
    daymap = {"Monday" : calendar.day_name[0], "Tuesday": calendar.day_name[1], "Wednesday" : calendar.day_name[2], \
        "Thursday" : calendar.day_name[3], "Friday" : calendar.day_name[4], "Saturday" : calendar.day_name[5], "Sunday" : calendar.day_name[6]}
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