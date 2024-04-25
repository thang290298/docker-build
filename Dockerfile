FROM alpine:3.7

LABEL maintainer="Carlos Augusto Malucelli <camalucelli@gmail.com>"

WORKDIR /webhook-alertmanager-telegram

RUN apk update \
                && apk add py3-pip bash gcc python3-dev musl-dev git libffi-dev openssl-dev \
                && rm -rf /var/cache/apk/* \
                && git clone https://github.com/thang290298/docker-build.git \
                && cd docker-build/  \
                && git checkout telegram-webhook-alert-python  \
                && pip3 install -r requirements.txt
                
WORKDIR /webhook-alertmanager-telegram

RUN chmod +x /webhook-alertmanager-telegram/run.sh

RUN chmod +x /webhook-alertmanager-telegram/flaskAlert.py

EXPOSE 9119

ENTRYPOINT ["./run.sh"]
