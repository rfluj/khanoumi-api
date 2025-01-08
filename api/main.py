from fastapi import FastAPI
from fastapi.responses import JSONResponse
from database.db import (
    connect_to_database, get_products, get_product_by_id,
    create_product, update_product, soft_delete_product,
    search_products_by_name, search_products_by_price_range
)
from typing import List
from .product import Product, ProductCreate
from decimal import Decimal
import json
from datetime import datetime

app = FastAPI()

# Database connection
connection = connect_to_database()

def custom_serializer(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def api_response(status: str, message: str, data=None, errors=None, status_code=200):
    content = {
        "status": status,
        "message": message,
        "data": data,
        "errors": errors,
    }
    # Use json.dumps with the custom serializer
    serialized_content = json.loads(json.dumps(content, default=custom_serializer))
    return JSONResponse(content=serialized_content, status_code=status_code)

@app.get("/products")
def read_products(limit: int = 10, offset: int = 0):
    products = get_products(connection, limit, offset)
    return api_response("success", "Products retrieved successfully", data=products)


@app.get("/products/{product_id}")
def read_product(product_id: int):
    product = get_product_by_id(connection, product_id)
    if not product:
        return api_response("fail", "Product not found", data=None, status_code=404)
    return api_response("success", "Product retrieved successfully", data=product)


@app.get("/products/search/name")
def read_products_by_name(name: str, limit: int = 10, offset: int = 0):
    """
    Search products by name (case-insensitive).
    """
    products = search_products_by_name(connection, name, limit, offset)
    if len(products) == 0:
        return api_response("fail", "No products found matching the name", data=None, status_code=404)
    return api_response("success", "Products retrieved successfully", data=products)


@app.get("/products/search/price")
def read_products_by_price_range(min_price: float, max_price: float, limit: int = 10, offset: int = 0):
    """
    Search products within a specific price range.
    """
    if min_price > max_price:
        return api_response("fail", "min_price must be less than or equal to max_price", data=None, status_code=400)
    products = search_products_by_price_range(connection, min_price, max_price, limit, offset)
    # if len(products) == 0:
    #     return JSONResponse(api_response("fail", "No products found in the given price range", data=None), status_code=404)
    return api_response("success", "Products retrieved successfully", data=products)



@app.post("/products")
def insert_product(product: ProductCreate):
    product_id = create_product(connection, product.dict())
    product = get_product_by_id(connection, product_id)
    return api_response("success", "Product created successfully", data=product)

@app.put("/products/{product_id}")
def update(product_id: int, product: ProductCreate):
    affected_rows = update_product(connection, product_id, product.dict())
    if affected_rows == 0:
        return api_response("fail", "Product not found or already deleted", data=None, status_code=404)
    product = get_product_by_id(connection, product_id)
    return api_response("success", "Product updated successfully", data=product)


@app.delete("/products/{product_id}")
def delete(product_id: int):
    affected_rows = soft_delete_product(connection, product_id)
    if not affected_rows:
        return api_response("fail", "Product not found or already deleted", data=None, status_code=404)
    return api_response("success", "Product deleted successfully", data=None)





