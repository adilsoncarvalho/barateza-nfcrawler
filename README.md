barateza/nfcrawler [![waffle.io dashboard](https://img.shields.io/badge/waffle.io-dashboard-brightgreen.svg)](https://waffle.io/adilsoncarvalho/barateza-nfcrawler)
===================

## Docker

We use Docker as our container engine and it should run smoothly on most
systems.

### Building the image locally

    docker build . -t barateza-nfcrawler
    docker-compose build
    docker-compose up --build

### Invoking the shell on the container

    docker run --rm -ti barateza-nfcrawler sh
    docker-compose run --rm scrapy sh

### Removing the image

    docker rmi barateza-nfcrawler
    docker-compose down

### Running the crawler

    docker run --rm -ti barateza-nfcrawler

#### Options as env vars

Pass them to the container using the `-e`/`--env` option. It is also possible
to pass them using a `--env-file` option.

- `LOGFILE` location for the log file (defaults to `/scrapy/nfcrawler/.scrapy/log/logfile.log`)
- `DATAFILE` location for the items file (defaults to `/scrapy/nfcrawler/.scrapy/data/items.json`)
