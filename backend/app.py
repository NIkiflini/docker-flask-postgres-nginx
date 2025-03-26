from flask import Flask, jsonify
import psycopg2
import os
import time

app = Flask(__name__)

# Database configuration
DB_HOST = os.getenv('DB_HOST', 'db')
DB_NAME = os.getenv('DB_NAME', 'mydatabase')
DB_USER = os.getenv('DB_USER', 'myuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'mypassword')

def get_db_connection():
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            # Create table if not exists
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL
                )
            """)
            # Insert sample data
            cur.execute("""
                INSERT INTO users (name, email)
                VALUES 
                    ('Alice', 'alice@example.com'),
                    ('Bob', 'bob@example.com')
                ON CONFLICT DO NOTHING
            """)
            conn.commit()
            return conn
        except psycopg2.OperationalError as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(retry_delay)

@app.route('/')
def hello():
    return 'Hello, World!', 200

@app.route('/health')
def health():
    return '', 200

@app.route('/users')
def get_users():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, name, email FROM users;')
        users = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{'id': user[0], 'name': user[1], 'email': user[2]} for user in users])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
