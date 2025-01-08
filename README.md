# Project Documentation: Khanoumi API

This project is a complete solution for scraping, storing, and managing skincare product data. It includes a web scraper to extract product data from a specified API and a FastAPI server to manage and query the data via RESTful APIs.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [How to Run](#how-to-run)
4. [Scraper Information](#scraper-information)
5. [API Information](#api-information)
6. [File Structure](#file-structure)

---

## Introduction

The application automates the following tasks:

- Scrapes skincare product details from a specified API.
- Stores the scraped data into a MySQL database.
- Provides a RESTful API server to manage and query the product data.

---

## Installation

### Prerequisites

1. Python 3.10+ installed on your system.
2. MySQL Server installed and running.
3. Install required Python packages by running:
   ```bash
   pip install -r requirements.txt
   ```

### Database Configuration

1. Open the `database/db.py` file.
2. Update the `DATABASE_CONFIG` dictionary with your MySQL credentials:

   ```python
   DATABASE_CONFIG = {
       "host": "localhost",
       "user": "your_username",
       "password": "your_password",
       "database": "your_database_name"
   }
   ```

---

## How to Run

### 1. Run the Scraper
To scrape skincare product data and save it into the database, run:

```bash
python scraper/scraper.py
```

### 2. Start the API Server
To start the FastAPI server for managing and querying product data:

```bash
uvicorn api.main:app --reload
```

### 3. Access API Documentation
- **Swagger**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Scraper Information

The scraper fetches skincare product data from the specified API and saves it to the database.

### Functions in `scraper.py`

#### 1. `scrape_products(connection, url)`
- Fetches product data from the provided URL.
- Parses the JSON response to extract product details (name, price, brand, etc.).
- Saves the data to the database.
- Logs errors if the scraping fails.

#### 2. `generate_product_url(slug)`
- Generates a full product URL using the product's slug.

#### 3. `create_url()`
- Constructs the API URL with pagination support.

#### 4. `main()`
- Handles database connection, table creation, and scraping workflow.
- Iterates through paginated API results to scrape all available products.

---

## API Information

The FastAPI server provides endpoints to manage and query product data.

### API Endpoints and Their Functions

#### 1. **Get All Products**
- **Endpoint**: `/products`
- **Method**: `GET`
- **Parameters**:
  - `limit`: Maximum number of products to fetch.
  - `offset`: Number of products to skip.
- **Response**: A list of products.

#### 2. **Get Product by ID**
- **Endpoint**: `/products/{product_id}`
- **Method**: `GET`
- **Response**: Details of the product with the given ID.

#### 3. **Search Products by Name**
- **Endpoint**: `/products/search/name`
- **Method**: `GET`
- **Parameters**:
  - `name`: Search term.
  - `limit`, `offset`: Pagination options.
- **Response**: A list of products matching the name.

#### 4. **Search Products by Price Range**
- **Endpoint**: `/products/search/price`
- **Method**: `GET`
- **Parameters**:
  - `min_price`: Minimum price.
  - `max_price`: Maximum price.
  - `limit`, `offset`: Pagination options.
- **Response**: A list of products in the specified price range.

#### 5. **Add a Product**
- **Endpoint**: `/products`
- **Method**: `POST`
- **Request Body**: Product details in JSON format.
- **Response**: The created product.

#### 6. **Update a Product**
- **Endpoint**: `/products/{product_id}`
- **Method**: `PUT`
- **Request Body**: Updated product details in JSON format.
- **Response**: The updated product.

#### 7. **Delete a Product**
- **Endpoint**: `/products/{product_id}`
- **Method**: `DELETE`
- **Response**: A success message if the product is deleted.

---

## File Structure

### 1. `scraper/scraper.py`
- Contains the scraper logic for fetching and saving product data.

### 2. `api/main.py`
- Implements the FastAPI server for managing and querying product data.

### 3. `database/db.py`
- Handles database connection, table creation, and saving data.

