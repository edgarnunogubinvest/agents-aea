FROM python:3.8-alpine

RUN apk add --no-cache make git bash

# cryptography: https://cryptography.io/en/latest/installation/#alpine
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev

# https://stackoverflow.com/a/57485724
RUN apk add --update --no-cache py3-numpy py3-scipy py3-pillow
ENV PYTHONPATH "$PYTHONPATH:/usr/lib/python3.7/site-packages"

# golang
RUN apk add --no-cache go

RUN pip install --upgrade pip
RUN pip install --upgrade --force-reinstall aea[all]==0.7.5

# COPY ./packages /home/packages # enable to add packages dir
WORKDIR home

WORKDIR /home/myagent

COPY deploy-image/entrypoint.sh /entrypoint.sh
COPY deploy-image/.aea "/root/.aea"
CMD [ "/entrypoint.sh" ]
