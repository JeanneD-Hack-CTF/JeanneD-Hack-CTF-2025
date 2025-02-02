#!/usr/bin/env python3

# Ne pas juger ce code dégueu svp x)
# Fait en speed avec l'ami gpt

from flask import Flask, request, make_response, render_template, redirect, url_for, session
from datetime import datetime, date

import os
import sqlite3
import logging
import werkzeug

# Disable logs color
werkzeug.serving._log_add_style = False

app = Flask(__name__)
app.secret_key = '3b834e34bc84a7205700f67e8d5904cd6991ffbdb9423270e2ccf6ce3c23bcd8'


LOGS_DIR = "logs"
DB_FILE = "users.db"
LOG_THRESHOLD = 1000


def log(msg: str, level="INFO"):
    logfile = os.path.join(LOGS_DIR, f"{date.today()}.log")
    with open(logfile, 'a') as f:
        f.write(f"[{level}] [{datetime.now()}] {msg}\n")


def init_db():
    log("Database initialisation")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    cursor.execute("""
        INSERT OR IGNORE INTO
            users (username, password, role)
        VALUES
            ('admin', 'adminaccountneedsaverystrongpassword', 'admin'),
            ('guest', 'password', 'guest'),
            ('jeannedhack', 'idkjustchooserandompassword!', 'guest')
    """)
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        log(f"Logging tentative as '{username}'")

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user'] = username
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('role', user[0])  # Cookie vulnérable à la modification
            log("Login successful")
            return resp

        log("Login error")
        return render_template('login.html', error="Identifiants incorrects")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('role', 'guest', max_age=0)
    return resp


@app.route('/admin')
def admin():
    if 'user' in session and request.cookies.get('role') == 'admin':
        return render_template('admin.html')
    else:
        log("Unauthorized access to /admin !")
        return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html', username=session['user'])


@app.route('/logs')
def logs():
    if 'user' in session and request.cookies.get('role') == 'admin':
        log_files = os.listdir(LOGS_DIR)
        return render_template('logs.html', log_files=log_files)
    else:
        return redirect(url_for('login'))


@app.route('/readlog')
def readlog():
    if 'user' in session and request.cookies.get('role') == 'admin':
        logfile = request.args.get('logfile', '')
        log(f"Read logs from : {logfile}")
        try:
            with open(os.path.join(LOGS_DIR, logfile), 'r') as f:
                logs = ''.join(f.readlines()[-40:])

            return render_template('readlog.html', content=logs)

        except Exception as e:
            return render_template('readlog.html', error=str(e))
    else:
        return redirect(url_for('login'))


@app.route('/users')
def users():
    if 'user' in session and request.cookies.get('role') == 'admin':
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT username, role FROM users")
        user_list = cursor.fetchall()
        conn.close()

        return render_template("users.html", users=user_list)

    log("Unauthorized access to /users !")
    return redirect(url_for('login'))


# --- Main ---

# Initialisation de la base de données
init_db()
    
if __name__ == '__main__':
    log("Application starting...")
    app.run(host="127.0.0.1")#0.0.0.0")

