import sqlite3
import os

DB_NAME = "su79_database.sqlite3"

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

# --- PRODUCTS TABLE ---
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
if not cursor.fetchone():
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
    print("Created 'products' table with 'category' column")
else:
    # Ensure category column exists
    cursor.execute("PRAGMA table_info(products)")
    columns = [col[1] for col in cursor.fetchall()]
    if "category" not in columns:
        cursor.execute("ALTER TABLE products ADD COLUMN category TEXT DEFAULT 'Uncategorized'")
        print("Added 'category' column to existing 'products' table")

# --- ADMIN TABLE ---
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='admin'")
if not cursor.fetchone():
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
    print("Created 'admin' table")

connection.commit()
connection.close()
print("Database initialized successfully")
