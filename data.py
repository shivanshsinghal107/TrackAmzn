import sqlite3

conn = sqlite3.connect("test.db")

conn.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INT NOT NULL, url TEXT NOT NULL, product_id VARCHAR(20) NOT NULL, title TEXT NOT NULL, tracking_price REAL, availability BIT NOT NULL, username VARCHAR(50), first_name VARCHAR(40), last_name VARCHAR(40))''')
conn.commit()
conn.close()