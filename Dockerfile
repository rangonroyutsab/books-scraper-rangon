FROM python:3.12-slim AS build-stage

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /workdir

RUN pip install --upgrade pip setuptools wheel \
    && pip install scrapyd-client

COPY books_scraper ./books_scraper

WORKDIR /workdir/books_scraper

RUN scrapyd-deploy --build-egg=/tmp/books_scraper.egg

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    OUTPUT_DIR=/app/outputs \
    DATA_DIR=/app/data

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    build-essential \
    ca-certificates \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

RUN mkdir -p \
    /etc/scrapyd \
    /var/lib/scrapyd/eggs/books_scraper \
    /var/lib/scrapyd/logs \
    /var/lib/scrapyd/items \
    /var/lib/scrapyd/dbs \
    /app/outputs \
    /app/data

COPY scrapyd.conf /etc/scrapyd/scrapyd.conf
COPY --from=build-stage /tmp/books_scraper.egg /var/lib/scrapyd/eggs/books_scraper/1.egg

EXPOSE 6800

CMD ["scrapyd", "--pidfile="]