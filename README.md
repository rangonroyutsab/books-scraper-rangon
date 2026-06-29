# Scrapy Assignment – Books to Scrape

## Project Overview

This is a Scrapy project built for scraping book information from [Books to Scrape](https://books.toscrape.com/index.html).

The spider starts from the homepage, finds the available book categories, goes through each category page, handles pagination, collects book links, and then randomly picks 5 books from every category. After visiting the selected book detail pages, it extracts the required information and sends the data through pipelines for cleaning, validation, database storage, and file export.

The project also includes Docker and Scrapyd setup so that the spider can be run locally or through the Scrapyd API.

## Features

The project includes the following features:

* Finds book categories dynamically from the website
* Does not use hardcoded category names or category URLs
* Visits all discovered category pages
* Handles pagination inside each category
* Collects book detail page URLs
* Randomly selects 5 books from every category
* Extracts book information such as:

  * `title`
  * `price`
  * `availability`
  * `product_url`
  * `image_url`
  * `category`
* Cleans the scraped data using Scrapy pipelines
* Removes the currency symbol from the price
* Converts price values into numeric format
* Converts availability text into boolean values
* Saves data into a SQLite database
* Exports the final data into:

  * JSON
  * CSV
  * XML

## Tech Stack

* Python
* Scrapy
* Scrapyd
* Scrapyd Client
* SQLite
* Docker

## Installation Guide

### 1. Clone the repository

```bash
git clone https://github.com/rangonroyutsab/books-scraper-rangon.git
cd books-scraper-rangon
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate the virtual environment.

For Linux or macOS:

```bash
source .venv/bin/activate
```

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Go to the Scrapy project directory

```bash
cd books_scraper
```

This directory contains the `scrapy.cfg` file, so Scrapy commands should be run from here.

### 5. Check the available spiders

```bash
scrapy list
```

Expected output:

```text
books
```

## Running the Spider Locally

Make sure you are inside the Scrapy project directory:

```bash
cd books_scraper
```

Run the spider:

```bash
scrapy crawl books
```

After the spider finishes running, the output files will be created inside the `outputs/` directory.

## Output Files

The project exports scraped data into three formats:

```text
books_scraper/
└── outputs/
    ├── books.json
    ├── books.csv
    └── books.xml
```

The project also stores the scraped data in a SQLite database:

```text
books_scraper/
└── data/
    └── books.db
```

## Output Format

Each scraped book record contains the following fields:

| Field          | Description                              | Example                                         |
| -------------- | ---------------------------------------- | ----------------------------------------------- |
| `title`        | Book title                               | `A Light in the Attic`                          |
| `price`        | Cleaned numeric price                    | `51.77`                                         |
| `availability` | Stock status as a boolean value          | `True`                                          |
| `product_url`  | Full URL of the book detail page         | `https://books.toscrape.com/catalogue/...`      |
| `image_url`    | Full URL of the book image               | `https://books.toscrape.com/media/cache/...jpg` |
| `category`     | Book category collected from the website | `Poetry`                                        |

### JSON example

```json
[
    {
        "title": "A Light in the Attic",
        "price": 51.77,
        "availability": true,
        "product_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
        "image_url": "https://books.toscrape.com/media/cache/...",
        "category": "Poetry"
    }
]
```

### CSV example

```csv
title,price,availability,product_url,image_url,category
A Light in the Attic,51.77,True,https://books.toscrape.com/catalogue/...,https://books.toscrape.com/media/cache/...,Poetry
```

### XML example

```xml
<items>
    <item>
        <title>A Light in the Attic</title>
        <price>51.77</price>
        <availability>True</availability>
        <product_url>https://books.toscrape.com/catalogue/...</product_url>
        <image_url>https://books.toscrape.com/media/cache/...</image_url>
        <category>Poetry</category>
    </item>
</items>
```

## Database Storage

The project uses a SQLite database through the `SQLiteStoragePipeline`.

Database path:

```text
books_scraper/data/books.db
```

Database table:

```text
books
```

Table structure:

| Column         | Type    | Description                            |
| -------------- | ------- | -------------------------------------- |
| `id`           | INTEGER | Auto-increment primary key             |
| `title`        | TEXT    | Book title                             |
| `price`        | REAL    | Book price after cleaning              |
| `availability` | INTEGER | `1` for in stock, `0` for out of stock |
| `product_url`  | TEXT    | Book detail page URL                   |
| `image_url`    | TEXT    | Book image URL                         |
| `category`     | TEXT    | Book category                          |

## Docker Setup

The project can also be run inside Docker with Scrapyd.

### 1. Build the Docker image

From the repository root:

```bash
docker build -t books-scraper-scrapyd .
```

### 2. Run the container

```bash
docker run -d -p 6800:6800 --name books-scraper books-scraper-scrapyd
```

### 3. Check Scrapyd status

```bash
curl http://localhost:6800/daemonstatus.json
```

Expected response:

```json
{
  "status": "ok"
}
```

### 4. Deploy the project to Scrapyd

Go to the Scrapy project directory:

```bash
cd books_scraper
```

Deploy the project:

```bash
scrapyd-deploy
```

### 5. Check deployed projects

```bash
curl http://localhost:6800/listprojects.json
```

Expected response:

```json
{
  "projects": ["books_scraper"],
  "status": "ok"
}
```

### 6. Check available spiders

```bash
curl "http://localhost:6800/listspiders.json?project=books_scraper"
```

Expected response:

```json
{
  "spiders": ["books"],
  "status": "ok"
}
```

### 7. Schedule the spider using Scrapyd

```bash
curl -X POST http://localhost:6800/schedule.json \
  -d project=books_scraper \
  -d spider=books
```

The response should include a `jobid`.

Example:

```json
{
  "jobid": "example-job-id",
  "status": "ok"
}
```

### 8. Check running and finished jobs

```bash
curl "http://localhost:6800/listjobs.json?project=books_scraper"
```

### 9. Stop and remove the Docker container

```bash
docker stop books-scraper
docker rm books-scraper
```

## Project Flow

```text
scrapy crawl books
        |
        v
Scrapy loads the project settings
        |
        v
BooksSpider starts from the homepage
        |
        v
Category links are collected dynamically
        |
        v
The spider visits each category page
        |
        v
Pagination links are followed
        |
        v
Book detail page URLs are collected
        |
        v
5 books are randomly selected from each category
        |
        v
The selected book pages are visited
        |
        v
Book data is extracted
        |
        v
The item is sent to pipelines
        |
        v
Data is cleaned and validated
        |
        v
Data is saved to SQLite
        |
        v
Scrapy exports data to JSON, CSV, and XML
```

## Folder Structure

```text
books-scraper-rangon/
├── books_scraper/
│   ├── books_scraper/
│   │   ├── spiders/
│   │   │   ├── __init__.py
│   │   │   └── books.py
│   │   ├── __init__.py
│   │   ├── items.py
│   │   ├── middlewares.py
│   │   ├── pipelines.py
│   │   └── settings.py
│   ├── data/
│   │   └── books.db
│   ├── outputs/
│   │   ├── books.csv
│   │   ├── books.json
│   │   └── books.xml
│   ├── scrapy.cfg
│   └── setup.py
├── .dockerignore
├── .gitignore
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
└── scrapyd.conf
```

## Important Implementation Details

### Dynamic category discovery

The spider collects category links from the sidebar of the homepage.

Selector used:

```python
response.css("div.side_categories ul.nav-list > li > ul > li > a")
```

This was done so that the spider does not depend on fixed category names. If the website adds or removes a category, the spider can still collect the current category list from the page.

### Spider and pipeline responsibilities

The spider handles the crawling part. It visits pages, follows links, collects raw values, and yields items.

The pipelines handle the processing part. They clean the scraped values, validate the required fields, and store the final data.

The main pipeline tasks are:

* clean extra spaces from text
* remove the pound sign from price values
* convert price into a numeric value
* convert availability into `True` or `False`
* check required fields
* save valid records into SQLite

## Known Limitations

* The scraper is made specifically for `books.toscrape.com`.
* The website is static, so this project does not handle JavaScript-rendered websites.
* SQLite is enough for this assignment, but PostgreSQL or MongoDB would be better for larger scraping projects.
* The project does not include proxy rotation.
* The project does not include automated tests yet.
* Repeated development runs may reuse cached responses if HTTP caching is enabled.

## Author

Rangon Roy Utsab


