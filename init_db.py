import sqlite3

DB_NAME = "su79_database.sqlite3"
connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

# Create products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL,
    image TEXT
)
""")
cursor.execute("SELECT COUNT(*) FROM products")
if cursor.fetchone()[0] == 0:
    cursor.execute(
        "INSERT INTO products (name, description, price, image) VALUES (?, ?, ?, ?)",
        ("Sample Product", "This is a test product.", 9.99, "https://via.placeholder.com/150")
    )

# Create admin table
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")
cursor.execute("SELECT COUNT(*) FROM admin")
if cursor.fetchone()[0] == 0:
    cursor.execute(
        "INSERT INTO admin (username, password) VALUES (?, ?)",
        ("admin", "admin123")  # Plaintext for testing only
    )

connection.commit()
connection.close()
print("Database initialized with 'products' and 'admin' tables")
