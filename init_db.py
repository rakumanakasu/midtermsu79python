import sqlite3
import os

DB_NAME = "su79_database.sqlite3"

# Only initialize if DB does not exist
if not os.path.exists(DB_NAME):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # Create products table with category
    cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL,
        image TEXT
    )
    """)
    cursor.execute(
        "INSERT INTO products (name, category, price, image) VALUES (?, ?, ?, ?)",
        ("Sample Product", "Test Category", 9.99, "https://via.placeholder.com/150")
    )

    # Create admin table
    cursor.execute("""
    CREATE TABLE admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)
    cursor.execute(
        "INSERT INTO admin (username, password) VALUES (?, ?)",
        ("admin", "admin123")  # Plaintext for testing only
    )

    connection.commit()
    connection.close()
    print("Database initialized with 'products' (with category) and 'admin' tables")
else:
    print("Database already exists, skipping init")
