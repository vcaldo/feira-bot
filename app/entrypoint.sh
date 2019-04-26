#!/bin/bash
/app/wait-for-elasticsearch.sh http://elasticsearch:9200 -- python /app/get-feiras.py 
python /app/feira-bot.py