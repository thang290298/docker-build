FROM alpine:3.7

LABEL maintainer="Carlos Augusto Malucelli <camalucelli@gmail.com>"

WORKDIR /webhook-alertmanager-telegram

RUN apk update \
                && apk add py3-pip bash gcc python3-dev musl-dev git libffi-dev openssl-dev \
                && rm -rf /var/cache/apk/* \
                && git clone https://github.com/thang290298/docker-build.git \
                && cd docker-build/  \
                && git checkout telegram-webhook-alert-python  \
                && pip install -r requirements.txt \
                && chmod +x run.sh

EXPOSE 9119

ENTRYPOINT ["./run.sh"]
