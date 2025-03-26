import psycopg2
import os

# Database configuration
DB_HOST = os.getenv('DB_HOST', 'db')
DB_NAME = os.getenv('DB_NAME', 'mydatabase')
DB_USER = os.getenv('DB_USER', 'myuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'mypassword')

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cur = conn.cursor()

# Create users table
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL
    )
''')

# Insert sample data
cur.execute('''
    INSERT INTO users (name, email)
    VALUES 
        ('Alice', 'alice@example.com'),
        ('Bob', 'bob@example.com')
    ON CONFLICT DO NOTHING
''')

conn.commit()
cur.close()
conn.close()
