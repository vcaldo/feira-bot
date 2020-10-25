FROM python:3.9-buster
COPY app/ /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "/app/entrypoint.sh" ]
