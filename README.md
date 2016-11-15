barateza/nfcrawler
===================

## Docker

We use Docker as our container engine and it should run smoothly on most
systems.

### Building the image locally

    docker build -t . barateza-nfcrawler
    docker-compose build
    docker-compose up --build

### Invoking the shell on the container

    docker run --rm -ti barateza-nfcrawler sh
    docker-compose run --rm scrapy sh

### Removing the image

    docker rmi barateza-nfcrawler
    docker-compose down
