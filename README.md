# Feira-bot
A Telegram bot that receives a location and reply with the nearby feiras livres of São Paulo.

## Usage

### Start elastic container
```
mkdir -p $HOME/esdata -p
chmod 777 $HOME/esdata
docker network create bot
docker run --detach --name elasticsearch --restart unless-stopped --volume $HOME/esdata:/usr/share/elasticsearch/data --network bot -e discovery.type=single-node -e "ES_JAVA_OPTS=-Xms200m -Xmx200m" docker.elastic.co/elasticsearch/elasticsearch:7.0.0
```
### Start bot container
```
docker run --detach --name bot --restart unless-stopped --network bot -e TELEGRAM_TOKEN=your_telegram_bot_token docker.io/vcaldo/feira-bot:latest
```
