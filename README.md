# Project Documentation: Khanoumi API

## Introduction

This API is designed to manage and interact with skincare product data. It provides functionalities such as:
- Retrieving products
- Searching by name or price range
- Creating, updating, and deleting products
- Error logging for better debugging and monitoring

---

## Prerequisites

- Python 3.10+
- MySQL Database
- Required Python libraries (listed in `requirements.txt`)

---

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-repository/khanoumi-api.git
cd khanoumi-api
```

### 2. Set Up the Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the Database
- Update the `DB_CONFIG` in `database/db.py` to match your MySQL configuration.

### 5. Run Migrations
Ensure the necessary tables (`skincare_products` and `errors`) are created:
```bash
python database/migrations.py
```

### 6. Start the Server
```bash
uvicorn api.main:app --reload --port 8000
```

### 7. Access the API Documentation
Open your browser and navigate to:  
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

### Products Endpoints

#### Retrieve All Products
**GET** `/products`

**Parameters:**  
- `limit` (int): Number of records to retrieve (default: 10)  
- `offset` (int): Pagination offset (default: 0)  

**Example:**  
```bash
curl "http://127.0.0.1:8000/products?limit=5&offset=0"
```

#### Retrieve a Product by ID
**GET** `/products/{product_id}`

**Example:**  
```bash
curl "http://127.0.0.1:8000/products/1"
```

#### Search Products by Name
**GET** `/products/search/name`

**Parameters:**  
- `name` (str): The product name (or partial name) to search for  
- `limit` (int): Number of records to retrieve  
- `offset` (int): Pagination offset  

**Example:**  
```bash
curl "http://127.0.0.1:8000/products/search/name?name=cream"
```

#### Search Products by Price Range
**GET** `/products/search/price`

**Parameters:**  
- `min_price` (float): Minimum price  
- `max_price` (float): Maximum price  
- `limit` (int): Number of records to retrieve  
- `offset` (int): Pagination offset  

**Example:**  
```bash
curl "http://127.0.0.1:8000/products/search/price?min_price=10&max_price=50"
```

#### Create a Product
**POST** `/products`

**Example Body:**  
```json
{
    "name": "Hydrating Cream",
    "basePrice": 25.99,
    "discountPrice": 20.99,
    "nameFa": "\u06a9\u0631\u0645 \u0622\u0628\u0631\u0633\u0627\u0646",
    "nameEn": "Hydrating Cream",
    "imageUrl": "http://example.com/image.jpg"
}
```

#### Update a Product
**PUT** `/products/{product_id}`

**Example Body:**  
```json
{
    "name": "Updated Hydrating Cream",
    "basePrice": 26.99,
    "discountPrice": 21.99,
    "nameFa": "\u06a9\u0631\u0645 \u0622\u0628\u0631\u0633\u0627\u0646 \u0628\u0647\u200c\u0631\u0648\u0632 \u0634\u062f\u0647",
    "nameEn": "Updated Hydrating Cream",
    "imageUrl": "http://example.com/new-image.jpg"
}
```

#### Soft Delete a Product
**DELETE** `/products/{product_id}`

**Example:**  
```bash
curl -X DELETE "http://127.0.0.1:8000/products/1"
```

---

### Error Logging

Errors related to database queries are automatically logged in the `errors` table. Each error entry includes:
- URL
- HTTP status code
- Error message
- Timestamp

---

## Project Structure

```
khanoumi-api/
├── api/
│   ├── main.py            # FastAPI main application
│   ├── product.py         # Pydantic models
│   ├── responses.py       # Custom API response structure
├── database/
│   ├── db.py              # Database connection and query functions
│   ├── migrations.py      # Script to set up database tables
├── tests/
│   ├── test_api.py        # API tests
│   ├── test_db.py         # Database query tests
├── requirements.txt       # Python dependencies
```

---

## Contributing

Feel free to open issues or submit pull requests for any enhancements or bug fixes.

---

## License

Include your license details here (e.g., MIT, Apache).

