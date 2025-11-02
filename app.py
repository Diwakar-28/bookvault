from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/books', methods=['GET'])
def get_books():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()

    books = [{"book_id": r[0], "title": r[1], "author": r[2], "price": r[3]} for r in rows]
    return jsonify(books)

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    price = data.get('price')

    if not title or not author or not price:
        return jsonify({"error": "Missing fields"}), 400

    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, price) VALUES (?, ?, ?)", (title, author, float(price)))
    conn.commit()
    conn.close()

    return jsonify({"message": "Book added successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)
