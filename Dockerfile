FROM python:3.7.0-slim-stretch
RUN apt-get update && apt-get install -y curl 
COPY app/ /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "/app/entrypoint.sh" ]