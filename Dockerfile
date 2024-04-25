FROM alpine:3.7

LABEL maintainer "Carlos Augusto Malucelli <malucellicarlos@gmail.com>"

RUN apk update \
                && apk add py3-pip bash gcc python3-dev musl-dev git libffi-dev openssl-dev \
                && rm -rf /var/cache/apk/* \
                && git clone https://github.com/thang290298/telegram-webhook-alert-python.git \
                && pip3 install -r telegram-webhook-alert-python/requirements.txt

WORKDIR /telegram-webhook-alert-python

RUN chmod +x /telegram-webhook-alert-python/run.sh

RUN chmod +x /telegram-webhook-alert-python/flaskAlert.py

EXPOSE 9119

ENTRYPOINT ["./run.sh"]