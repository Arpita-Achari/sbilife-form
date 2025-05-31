from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key

DB_FILE = 'sbilife.db'

# Ensure database and table exist
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, mobile TEXT, email TEXT, address TEXT,
        dob TEXT, mother TEXT, father TEXT, qualification TEXT,
        occupation TEXT, company TEXT, work_type TEXT, designation TEXT,
        service_length TEXT, height TEXT, weight TEXT, birth_place TEXT,
        income TEXT, nominee TEXT, nominee_dob TEXT,
        vaccine1 TEXT, vaccine2 TEXT,
        pan TEXT, aadhar TEXT, account TEXT, ifsc TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = (
            request.form['name'],
            request.form['mobile'],
            request.form['email'],
            request.form['address'],
            request.form['dob'],
            request.form['mother'],
            request.form['father'],
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
            request.form['nominee'],
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
            name, mobile, email, address, dob, mother, father,
            qualification, occupation, company, work_type, designation,
            service_length, height, weight, birth_place, income,
            nominee, nominee_dob, vaccine1, vaccine2, pan, aadhar,
            account, ifsc
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
        conn.commit()
        conn.close()
        return render_template("thankyou.html")
    return render_template("form.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Replace with your desired login credentials
        if username == 'admin' and password == 'admin123':
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
    init_db()
    app.run(debug=True)
