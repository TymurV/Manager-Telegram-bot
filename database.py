import sqlite3
from config import DATABASE

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            name TEXT NOT NULL,
            description TEXT,
            image_path TEXT,
            recomended_age TEXT,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')
    
    cursor.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (1, '11-15 лет')")
    cursor.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (2, '8-13 лет')")
    cursor.execute("INSERT OR IGNORE INTO products (id, category_id, name, description, image_path, recomended_age) VALUES (1, 1, 'Курс Python', 'Изучите Python с нуля!', 'images/PYTHON.png', '11-13')")
    cursor.execute("INSERT OR IGNORE INTO products (id, category_id, name, description, image_path, recomended_age) VALUES (2, 1, 'Курс Java', 'Погрузитесь в мир Java!', 'images/JAVA.png', '12-15')")
    cursor.execute("INSERT OR IGNORE INTO products (id, category_id, name, description, image_path, recomended_age) VALUES (3, 2, 'Курс UI/UX', 'Создавайте крутые интерфейсы!', 'images/UI_UX.png', '8-13')")
    
    conn.commit()
    conn.close()

def save_user(telegram_id, username):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?)", (telegram_id, username))
    conn.commit()
    conn.close()

def get_categories():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()
    conn.close()
    return categories

def get_products(category_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM products WHERE category_id = ?", (category_id,))
    products = cursor.fetchall()
    conn.close()
    return products

def get_product(product_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, description, recomended_age, image_path FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product