from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from flask import Request

# Limit form data size (1MB)
Request.max_form_memory_size = 1024 * 1024

app = Flask(__name__)
app.secret_key = 'raj@0632'  # Replace with a secure key

DB_FILE = 'sbilife.db'

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS customers')  # Reset table each time app restarts (for dev only)
    c.execute('''CREATE TABLE customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, mobile TEXT, email TEXT, address TEXT,
        dob TEXT, mother_name TEXT, father_name TEXT, qualification TEXT,
        occupation TEXT, company TEXT, work_type TEXT, designation TEXT,
        service_length TEXT, height TEXT, weight TEXT, birth_place TEXT,
        income TEXT, nominee_name TEXT, nominee_dob TEXT,
        vaccine1 TEXT, vaccine2 TEXT,
        pan TEXT, aadhar TEXT, account TEXT, ifsc TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            data = (
                request.form['name'],
                request.form['mobile'],
                request.form['email'],
                request.form['address'],
                request.form['dob'],
                request.form['mother_name'],
                request.form['father_name'],
                request.form['qualification'],
                request.form['occupation'],
                request.form['company'],
                request.form['work_type'],
                request.form['designation'],
                request.form['service_length'],
                request.form['height'],
                request.form['weight'],
                request.form['birth_place'],
                request.form['income'],
                request.form['nominee_name'],
                request.form['nominee_dob'],
                request.form['vaccine1'],
                request.form['vaccine2'],
                request.form['pan'],
                request.form['aadhar'],
                request.form['account'],
                request.form['ifsc']
            )

            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute('''INSERT INTO customers (
                name, mobile, email, address, dob, mother_name, father_name,
                qualification, occupation, company, work_type, designation,
                service_length, height, weight, birth_place, income,
                nominee_name, nominee_dob, vaccine1, vaccine2, pan, aadhar,
                account, ifsc
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
            conn.commit()
            conn.close()
            return render_template("thankyou.html")
        except Exception as e:
            return f"⚠️ Bad Request Error: {e}", 400
    return render_template("form.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("Received form data:", request.form)
        username = request.form['username']
        password = request.form['password']
        if username == 'Rajashree' and password == 'raj@0632':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials. Please try again.")
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM customers")
    rows = c.fetchall()
    conn.close()
    return render_template("dashboard.html", rows=rows)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()  # Creates fresh table on every run — remove in production!
    app.run(debug=True)
