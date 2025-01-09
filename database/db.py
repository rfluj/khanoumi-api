import mysql.connector

# MySQL Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "khanoumi",
}

def connect_to_database():
    """Connect to MySQL database."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        """Create a table to log errors with URLs and status codes."""
        query = """
        CREATE TABLE IF NOT EXISTS errors (
            id INT AUTO_INCREMENT PRIMARY KEY,
            url TEXT NOT NULL,
            statusCode INT NOT NULL,
            errorMessage TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        print("Connected to the database.")
        print("Table `errors` created or already exists.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def log_error(connection, url, status_code, error_message=None):
    """Insert an error entry into the errors table."""
    try:
        query = """
        INSERT INTO errors (url, statusCode, errorMessage)
        VALUES (%s, %s, %s)
        """
        cursor = connection.cursor()
        cursor.execute(query, (url, status_code, error_message))
        connection.commit()
        cursor.close()
        print(f"Logged error for URL: {url} with status code: {status_code}")
    except mysql.connector.Error as err:
        print(f"Failed to log error: {err}")

def create_table(connection):
    """Create a table to store product details."""
    try:
        query = """
        CREATE TABLE IF NOT EXISTS skincare_products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            url VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            discountPrice DECIMAL(20),
            basePrice DECIMAL(20),
            nameFa TEXT,
            nameEn TEXT,
            imageUrl TEXT,
            createTime DATETIME DEFAULT CURRENT_TIMESTAMP,
            updateTime DATETIME DEFAULT CURRENT_TIMESTAMP,
            deleteTime DATETIME DEFAULT NULL,
            isDeleted BOOLEAN DEFAULT FALSE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        print("Table `skincare_products` created or already exists.")
    except mysql.connector.Error as err:
        log_error(connection, "create_table", 500, str(err))
        print(f"Error creating table: {err}")

def save_to_database(connection, product):
    """Save scraped products to the database."""
    try:
        query = """
        INSERT INTO skincare_products (url, name, discountPrice, basePrice, nameFa, nameEn, imageUrl)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor = connection.cursor()
        cursor.execute(query, (product["productUrl"], product["name"], product["discountPrice"], product["basePrice"], product["nameFa"], product["nameEn"], product["imageUrl"]))
        connection.commit()
        cursor.close()
        print(f'Product saved to the database. name: {product["name"]}')
    except mysql.connector.Error as err:
        log_error(connection, product.get("productUrl", "Unknown URL"), 500, str(err))
        print(f"Error saving product: {err}")

def get_products(connection, limit=10, offset=0):
    """
    Retrieve a list of products with pagination.
    """
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM skincare_products WHERE isDeleted = FALSE LIMIT %s OFFSET %s"
        cursor.execute(query, (limit, offset))
        products = cursor.fetchall()
        cursor.close()
        return products
    except mysql.connector.Error as err:
        log_error(connection, "get_products", 500, str(err))
        print(f"Error retrieving products: {err}")
        return []

def get_product_by_id(connection, product_id):
    """
    Retrieve a single product by ID.
    """
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM skincare_products WHERE id = %s AND isDeleted = FALSE"
        cursor.execute(query, (product_id,))
        product = cursor.fetchone()
        cursor.close()
        return product
    except mysql.connector.Error as err:
        log_error(connection, f"get_product_by_id_{product_id}", 500, str(err))
        print(f"Error retrieving product: {err}")
        return None

def search_products_by_name(connection, name, limit=10, offset=0):
    """
    Search products by name (case-insensitive).
    """
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT * FROM skincare_products
        WHERE (name LIKE %s)
        AND isDeleted = FALSE
        LIMIT %s OFFSET %s
        """
        search_term = f"%{name}%"
        cursor.execute(query, (search_term, limit, offset))
        products = cursor.fetchall()
        cursor.close()
        return products
    except mysql.connector.Error as err:
        log_error(connection, f"search_products_by_name_{name}", 500, str(err))
        print(f"Error searching products by name: {err}")
        return []

def search_products_by_price_range(connection, min_price, max_price, limit=10, offset=0):
    """
    Search products within a specific price range.
    """
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT * FROM skincare_products
        WHERE basePrice BETWEEN %s AND %s
        AND isDeleted = FALSE
        LIMIT %s OFFSET %s
        """
        cursor.execute(query, (min_price, max_price, limit, offset))
        products = cursor.fetchall()
        cursor.close()
        return products
    except mysql.connector.Error as err:
        log_error(connection, "search_products_by_price_range", 500, str(err))
        print(f"Error searching products by price range: {err}")
        return []

def create_product(connection, product_data):
    """
    Create a new product.
    """
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO skincare_products (url, name, discountPrice, basePrice, nameFa, nameEn, imageUrl)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            product_data["url"],
            product_data["name"], product_data["discountPrice"], product_data["basePrice"],
            product_data["nameFa"], product_data["nameEn"], product_data["imageUrl"]
        ))
        connection.commit()
        product_id = cursor.lastrowid
        cursor.close()
        return product_id
    except mysql.connector.Error as err:
        log_error(connection, "create_product", 500, str(err))
        print(f"Error creating product: {err}")
        return None

def update_product(connection, product_id, product_data):
    """
    Update an existing product.
    """
    try:
        cursor = connection.cursor()
        query = """
        UPDATE skincare_products
        SET url = %s, name = %s, discountPrice = %s, basePrice = %s, nameFa = %s, nameEn = %s, imageUrl = %s, updateTime = CURRENT_TIMESTAMP
        WHERE id = %s AND isDeleted = FALSE
        """
        cursor.execute(query, (
            product_data["url"],
            product_data["name"], product_data["discountPrice"], product_data["basePrice"],
            product_data["nameFa"], product_data["nameEn"], product_data["imageUrl"], product_id
        ))
        connection.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        return affected_rows
    except mysql.connector.Error as err:
        log_error(connection, f"update_product_{product_id}", 500, str(err))
        print(f"Error updating product: {err}")
        return 0

def soft_delete_product(connection, product_id):
    """Soft delete a product by setting isDeleted to TRUE and deleteTime."""
    try:
        # Check if the product is already deleted
        check_query = "SELECT isDeleted FROM skincare_products WHERE id = %s"
        cursor = connection.cursor(dictionary=True)
        cursor.execute(check_query, (product_id,))
        product = cursor.fetchone()
        if not product:
            cursor.close()
            return False
        if product["isDeleted"] == 1:
            cursor.close()
            return False
        query = """
        UPDATE skincare_products
        SET isDeleted = TRUE, deleteTime = CURRENT_TIMESTAMP
        WHERE id = %s
        """
        cursor = connection.cursor()
        cursor.execute(query, (product_id,))
        connection.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        return affected_rows
    except mysql.connector.Error as err:
        log_error(connection, f"soft_delete_product_{product_id}", 500, str(err))
        print(f"Error deleting product: {err}")


