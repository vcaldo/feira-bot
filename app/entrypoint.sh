#!/bin/bash
sleep 20
echo "`date +\"%D %T\"` - feira-bot - Loading feira data to elasticsearch"
python /app/get-feiras.py &&
echo "`date +\"%D %T\"` - feira-bot - Data loaded sucessful."