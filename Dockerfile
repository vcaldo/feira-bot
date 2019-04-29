FROM python:3.7.0-slim-stretch
RUN apt-get update && apt-get install -y locales curl 
RUN sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=pt_BR.UTF-8
ENV LANG pt_BR.UTF-8 
ENV TZ=America/Sao_Paulo
COPY app/ /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "/app/entrypoint.sh" ]