#!/bin/sh

LOGFILE=${LOGFILE:-/scrapy/nfcrawler/.scrapy/log/logfile.log}
DATAFILE=${DATAFILE:-/scrapy/nfcrawler/.scrapy/data/items.json}

mkdir -p $(dirname "${LOGFILE}")
mkdir -p $(dirname "${DATAFILE}")

scrapy crawl pr-nfce \
  --logfile=$LOGFILE \
  --output=$DATAFILE \
  --output-format=jsonlines
