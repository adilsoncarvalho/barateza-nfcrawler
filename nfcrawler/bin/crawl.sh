#!/bin/sh

LOGFILE=${LOGFILE:-/scrapy/nfcrawler/.scrapy/log/logfile.log}

mkdir -p $(dirname "${LOGFILE}")

scrapy crawl pr-nfce \
  --logfile $LOGFILE
