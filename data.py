import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Set up database
engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///database.db"))
db = scoped_session(sessionmaker(bind=engine))

db.execute('''CREATE TABLE IF NOT EXISTS products (id SERIAL PRIMARY KEY, user_id INT NOT NULL, url TEXT NOT NULL, product_id VARCHAR(20) NOT NULL, title TEXT NOT NULL, tracking_price REAL, availability BOOLEAN NOT NULL, username VARCHAR(50), first_name VARCHAR(40), last_name VARCHAR(40))''')

db.commit()
db.close()
