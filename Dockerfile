FROM python:2.7-alpine

RUN apk update
RUN apk add curl libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev

RUN pip install scrapy

RUN mkdir -p /scrapy
COPY . /scrapy
WORKDIR /scrapy/nfcrawler

CMD ["bin/crawl.sh"]
