# MCdonalds

# Product Scraper API

This project is a FastAPI based backend service that collects product data from MCdonalds menu, processes it in parallel, caches the results in a local JSON file and provides API endpoints to access product information.

---

## Features

- Scrapes all products from the menu page concurrently using `ThreadPoolExecutor`.
- Parses detailed product information with Playwright and BeautifulSoup.
- Caches scraped data locally in a JSON file (`data/items.json`).
- Provides FastAPI endpoints:
  - `GET /all_products/` — returns all products data.
  - `GET /products/{product_name}` — returns details of a product.
  - `GET /products/{product_name}/{product_field}` — returns specific field of a product.

***Attempted to do via asynchronous implementation, but ran into problems closing event loop and `I/O operation on closed pipe` errors. So it was decided to use threads.***

---

## Requirements

- Python 3.10+
- FastAPI
- Uvicorn
- Playwright
- BeautifulSoup4
- Other dependencies as listed in `requirements.txt`

---