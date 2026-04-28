# Contact Management System (First Project)
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS member (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT,
            lastname TEXT,
            gender TEXT,
            age INTEGER,
            address TEXT,
            contact TEXT
        )
    """)
    conn.commit()
    conn.close()

# Home page - show all contacts
@app.route('/')
def index():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM member")
    contacts = cursor.fetchall()
    conn.close()
    return render_template("index.html", contacts=contacts)

# Add new contact
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = (
            request.form['firstname'],
            request.form['lastname'],
            request.form['gender'],
            request.form['age'],
            request.form['address'],
            request.form['contact']
        )
        conn = sqlite3.connect("contacts.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO member VALUES (NULL,?,?,?,?,?,?)", data)
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template("add.html")

# Edit contact
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()

    if request.method == 'POST':
        cursor.execute("""
            UPDATE member 
            SET firstname=?, lastname=?, gender=?, age=?, address=?, contact=? 
            WHERE id=?
        """, (
            request.form['firstname'],
            request.form['lastname'],
            request.form['gender'],
            request.form['age'],
            request.form['address'],
            request.form['contact'],
            id
        ))
        conn.commit()
        conn.close()
        return redirect('/')

    cursor.execute("SELECT * FROM member WHERE id=?", (id,))
    contact = cursor.fetchone()
    conn.close()
    return render_template("edit.html", contact=contact)

# Delete contact
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM member WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Run app
if __name__ == "__main__":
    init_db()
    app.run(debug=True)