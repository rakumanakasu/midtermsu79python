import sqlite3

DB_NAME = "su79_database.sqlite3"

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

# Create products table if it does not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL,
    image TEXT
)
""")

# Insert sample product if table empty
cursor.execute("SELECT COUNT(*) FROM products")
if cursor.fetchone()[0] == 0:
    cursor.execute(
        "INSERT INTO products (name, description, price, image) VALUES (?, ?, ?, ?)",
        ("Sample Product", "This is a test product.", 9.99, "https://via.placeholder.com/150")
    )

# Create admin table if it does not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

# Insert sample admin if table empty
cursor.execute("SELECT COUNT(*) FROM admin")
if cursor.fetchone()[0] == 0:
    cursor.execute(
        "INSERT INTO admin (username, password) VALUES (?, ?)",
        ("admin", "123")  # Use hashed passwords in real projects!
    )

connection.commit()
connection.close()
print("Database initialized with 'products' and 'admin' tables.")
