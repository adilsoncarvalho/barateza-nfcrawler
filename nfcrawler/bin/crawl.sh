#!/bin/sh

LOGFILE=${LOGFILE:-/scrapy/nfcrawler/.scrapy/log/logfile.log}
DATAFILE=${DATAFILE:-/scrapy/nfcrawler/.scrapy/data/items.json}
CACHEDIR=${CACHEDIR:-/scrapy/nfcrawler/.scrapy/httpcache}

mkdir -p $(dirname "${LOGFILE}")
mkdir -p $(dirname "${DATAFILE}")
mkdir -p $CACHEDIR

scrapy crawl pr-nfce \
  --logfile=$LOGFILE \
  --output=$DATAFILE \
  --output-format=jsonlines \
  --set HTTPCACHE_ENABLED=1 \
  --set HTTPCACHE_DIR=$CACHEDIR \
  --set HTTPCACHE_STORAGE=scrapy.extensions.httpcache.FilesystemCacheStorage
