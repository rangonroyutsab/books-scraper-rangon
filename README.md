# Scrapy Assignment – Books to Scrape

## Project Overview

This project is a Scrapy-based web scraping application for extracting book data from [Books to Scrape](https://books.toscrape.com/index.html).

The scraper starts from the homepage, discovers all available book categories dynamically, visits each category, collects book URLs, randomly selects books from each category, extracts required product information, cleans the data through Scrapy pipelines, exports the final dataset into multiple formats, and supports deployment through Scrapyd and Docker.


## Features

* Dynamically discovers all book categories from the homepage
* Avoids hardcoded category names and category URLs
* Visits each discovered category page
* Handles category pagination
* Collects book detail page URLs from each category
* Randomly selects books from each category
* Extracts the following fields:

  * `title`
  * `price`
  * `availability`
  * `product_url`
  * `image_url`
  * `category`
* Cleans and normalizes scraped data using Scrapy pipelines
* Removes currency symbols from prices
* Converts price values into numeric format
* Converts availability text into boolean format
* Exports scraped data into:

  * JSON
  * CSV
  * XML
* Supports SQLite database storage through a Scrapy pipeline
* Uses a custom downloader middleware for User-Agent rotation
* Supports running locally using Scrapy
* Supports deployment and execution through Scrapyd
* Supports containerized deployment using Docker

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

Activate the virtual environment:

For Linux/macOS:

```bash
source .venv/bin/activate
```

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install project dependencies

```bash
pip install -r requirements.txt
```

### 4. Move into the Scrapy project directory

```bash
cd books_scraper
```

This is the directory that contains `scrapy.cfg`.

### 5. Verify the available spiders

```bash
scrapy list
```

Expected spider:

```bash
books
```

## Environment Setup

The project uses default local paths for output files and database files.

When running locally, generated files are stored inside the Scrapy project directory:

```text
books_scraper/
├── outputs/
│   ├── books.json
│   ├── books.csv
│   └── books.xml
└── data/
    └── books.db
```

The output and database paths are configured in `books_scraper/books_scraper/settings.py`.

```python
PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", PROJECT_ROOT / "outputs"))
DATA_DIR = Path(os.getenv("DATA_DIR", PROJECT_ROOT / "data"))

BOOKS_SQLITE_PATH = str(DATA_DIR / "books.db")
```

Optional environment variables:


## Running the Spider

Make sure you are inside the Scrapy project directory:

```bash
cd books_scraper
```

Run the spider:

```bash
scrapy crawl books
```


## Docker Setup Guide

The project includes a Dockerfile and Scrapyd configuration for containerized deployment.

### 1. Build the Docker image

From the repository root:

```bash
docker build -t books-scraper-scrapyd .
```

### 2. Run the container

```bash
docker run -d -p 6800:6800 --name books-scraper books-scraper-scrapyd
```

### 3. Verify Scrapyd is running

```bash
curl http://localhost:6800/daemonstatus.json
```

Expected response:

```json
{
  "status": "ok"
}
```

### 4. Deploy the Scrapy project to Scrapyd

From the repository root:

```bash
cd books_scraper
scrapyd-deploy
```

### 5. Verify deployed projects

```bash
curl http://localhost:6800/listprojects.json
```

Expected project:

```json
{
  "status": "ok",
  "projects": ["books_scraper"]
}
```

### 6. Verify available spiders

```bash
curl "http://localhost:6800/listspiders.json?project=books_scraper"
```

Expected spider:

```json
{
  "status": "ok",
  "spiders": ["books"]
}
```

### 7. Schedule the spider through Scrapyd API

```bash
curl -X POST http://localhost:6800/schedule.json \
  -d project=books_scraper \
  -d spider=books
```

The response will contain a `jobid`.

Example:

```json
{
  "status": "ok",
  "jobid": "example-job-id"
}
```

### 8. Check job status

```bash
curl "http://localhost:6800/listjobs.json?project=books_scraper"
```

### 9. Stop and remove the Docker container

```bash
docker stop books-scraper
docker rm books-scraper
```

## Output Format Description

The project exports scraped book data into three formats using Scrapy Feed Exports.

The configured output files are:

```text
outputs/books.json
outputs/books.csv
outputs/books.xml
```

Each exported record contains the following fields:

| Field          | Description                               | Example                                         |
| -------------- | ----------------------------------------- | ----------------------------------------------- |
| `title`        | Book title                                | `A Light in the Attic`                          |
| `price`        | Cleaned numeric price                     | `51.77`                                         |
| `availability` | Boolean stock status                      | `True`                                          |
| `product_url`  | Absolute URL of the book detail page      | `https://books.toscrape.com/catalogue/...`      |
| `image_url`    | Absolute URL of the book image            | `https://books.toscrape.com/media/cache/...jpg` |
| `category`     | Category name discovered from the website | `Poetry`                                        |

### JSON output

The JSON file contains an array of book objects.

Example:

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

### CSV output

The CSV file stores the same fields in tabular format.

Example:

```csv
title,price,availability,product_url,image_url,category
A Light in the Attic,51.77,True,https://books.toscrape.com/catalogue/...,https://books.toscrape.com/media/cache/...,Poetry
```

### XML output

The XML file stores each book inside an `<item>` element.

Example:

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

## Database Configuration

The project includes SQLite database storage support through the `SQLiteStoragePipeline`.

Database path:

```text
books_scraper/data/books.db
```

Database table:

```text
books
```

Table columns:

| Column         | Type    | Description                            |
| -------------- | ------- | -------------------------------------- |
| `id`           | INTEGER | Auto-increment primary key             |
| `title`        | TEXT    | Book title                             |
| `price`        | REAL    | Numeric book price                     |
| `availability` | INTEGER | `1` for in stock, `0` for out of stock |
| `product_url`  | TEXT    | Book detail page URL                   |
| `image_url`    | TEXT    | Book image URL                         |
| `category`     | TEXT    | Book category                          |

To enable full validation and SQLite storage, make sure the pipeline settings include:

```python
ITEM_PIPELINES = {
    "books_scraper.pipelines.CleanDataPipeline": 300,
    "books_scraper.pipelines.ValidationPipeline": 350,
    "books_scraper.pipelines.SQLiteStoragePipeline": 400,
}
```

To inspect database records after running the spider:

```bash
python - <<'PY'
import sqlite3

conn = sqlite3.connect("data/books.db")
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM books")
print("Total records:", cur.fetchone()[0])

cur.execute("SELECT title, price, availability, category FROM books LIMIT 5")
for row in cur.fetchall():
    print(row)

conn.close()
PY
```

## Architecture Diagram

```text
scrapy crawl books
        |
        v
scrapy.cfg
        |
        v
settings.py
        |
        v
Load Spider, Middleware, and Pipelines
        |
        v
BooksSpider
        |
        v
Start URL:
https://books.toscrape.com/index.html
        |
        v
Discover categories dynamically
        |
        v
Visit category pages
        |
        v
Follow pagination
        |
        v
Collect book detail URLs
        |
        v
Randomly select books from category
        |
        v
Visit selected book detail pages
        |
        v
Extract item fields
        |
        v
BookItem
        |
        v
CleanDataPipeline
        |
        v
ValidationPipeline
        |
        v
SQLiteStoragePipeline
        |
        v
Feed Exports + SQLite Database
        |
        v
JSON / CSV / XML / books.db
```

## Folder Structure

Project structure:

```text
books-scraper-rangon/
├── books_scraper/
│   ├── books_scraper/
│   │   ├── __init__.py
│   │   ├── items.py
│   │   ├── middlewares.py
│   │   ├── pipelines.py
│   │   ├── settings.py
│   │   └── spiders/
│   │       ├── __init__.py
│   │       └── books.py
│   ├── data/
│   │   └── books.db
│   ├── outputs/
│   │   ├── books.csv
│   │   ├── books.json
│   │   └── books.xml
│   ├── scrapy.cfg
│   └── setup.py
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
└── scrapyd.conf
```

Files and folders that should not be committed:

```text
__pycache__/
*.pyc
.scrapy/
httpcache/
*.egg-info/
.eggs/
build/
dist/
```


## Design Decisions

### Dynamic category discovery

The spider extracts category links from the homepage instead of hardcoding category names or URLs.

Selector used:

```python
response.css("div.side_categories ul.nav-list > li > ul > li > a")
```

This allows the scraper to continue working if categories are added or removed from the website.

### Separate spider and pipeline responsibilities

The spider is responsible for:

* Crawling pages
* Extracting raw values
* Following links
* Yielding structured items

The pipeline is responsible for:

* Cleaning text
* Removing currency symbols
* Converting price to numeric format
* Converting availability to boolean format
* Validating required fields
* Storing data in SQLite

This keeps the code modular and easier to maintain.




## Known Limitations

* The scraper is designed specifically for `books.toscrape.com`.
* The website is static; this project does not handle JavaScript-rendered pages.
* Random selection means each full run may produce different selected books.
* Some categories may contain fewer than five books. In that case, the spider should select all available books from that category.
* SQLite is suitable for this assignment and small datasets, but MongoDB or PostgreSQL would be better for larger production scraping systems.
* HTTP caching may cause repeated development runs to reuse cached pages unless disabled.
* The project does not currently include automated tests.
* The project does not include proxy rotation.

