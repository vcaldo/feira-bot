#!/bin/bash
sleep 15
echo "`date +\"%D %T\"` - feira-bot - Loading feira data to elasticsearch"
python /app/get-feiras.py &&
echo "`date +\"%D %T\"` - feira-bot - Data loaded sucessful."
python /app/feira-bot.py &&
echo "`date +\"%D %T\"` - feira-bot - Bot started!"