import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

DB_PATH = Path('database/hotel.db')

MENU_ITEMS = [
    ('Pancake Stack', 'Breakfast', 'Fluffy pancakes served with fruit and syrup.', 650, '🥞'),
    ('Full English Breakfast', 'Breakfast', 'Eggs, sausage, toast, beans and grilled tomato.', 950, '🍳'),
    ('Avocado Toast', 'Breakfast', 'Toasted bread topped with fresh avocado.', 700, '🥑'),
    ('Grilled Chicken', 'Lunch', 'Grilled chicken served with seasoned potatoes.', 1250, '🍗'),
    ('Beef Burger', 'Lunch', 'Beef patty, lettuce, tomato and house sauce.', 1100, '🍔'),
    ('Chicken Biryani', 'Lunch', 'Fragrant rice with spiced chicken.', 1200, '🍛'),
    ('Grilled Fish', 'Dinner', 'Fresh fish served with vegetables.', 1450, '🐟'),
    ('Beef Steak', 'Dinner', 'Tender steak with chips and vegetables.', 1800, '🥩'),
    ('Vegetable Pasta', 'Dinner', 'Pasta tossed with seasonal vegetables.', 1150, '🍝'),
    ('Fresh Orange Juice', 'Drinks', 'Freshly squeezed orange juice.', 350, '🍊'),
    ('Iced Coffee', 'Drinks', 'Chilled coffee served over ice.', 400, '🧋'),
    ('Mineral Water', 'Drinks', 'Bottled drinking water.', 150, '💧'),
    ('Chocolate Cake', 'Dessert', 'Rich chocolate cake slice.', 450, '🍰'),
    ('Fruit Salad', 'Dessert', 'A refreshing bowl of seasonal fruits.', 400, '🍓'),
    ('Vanilla Ice Cream', 'Dessert', 'Two scoops of vanilla ice cream.', 350, '🍨'),
]

def get_db(db_path=None):
    path = db_path or DB_PATH
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute('PRAGMA foreign_keys = ON')
    return connection

def init_db(db_path=None):
    db = get_db(db_path)
    db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            emoji TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            delivery_address TEXT NOT NULL,
            total REAL NOT NULL,
            payment_method TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Received',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        );
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
            comment TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    ''')
    count = db.execute('SELECT COUNT(*) FROM menu_items').fetchone()[0]
    if count == 0:
        db.executemany('INSERT INTO menu_items (name, category, description, price, emoji) VALUES (?, ?, ?, ?, ?)', MENU_ITEMS)
    db.commit()
    db.close()
