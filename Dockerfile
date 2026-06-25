FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    curl \
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

COPY . .

RUN mkdir -p \
    /var/lib/scrapyd/eggs \
    /var/lib/scrapyd/logs \
    /var/lib/scrapyd/items \
    /var/lib/scrapyd/dbs \
    /app/outputs \
    /app/data

COPY scrapyd.conf /etc/scrapyd/scrapyd.conf

EXPOSE 6800

CMD ["scrapyd", "--pidfile="]