from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_session import Session
import sqlite3

app = Flask('__name__')
app.config['SESSION_TYPE'] = 'filesystem'
app.config["SESSION_PERMANENT"] = False
app.secret_key = 'iuuirg&&@84i0g@1h94t&189g4@8172g'

Session(app)

@app.route('/')
def index():
  return render_template('index.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route('/login', methods=['POST', 'GET'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    
    user = cursor.fetchone()
    conn.close()

    if user is not None:
      session["username"] = username
      session["password"] = password

      return redirect(url_for('login'))
    else:
      flash('Usuário ou senha incorretos.')
    return redirect(url_for('index'))

  if session.get('username'):
    return redirect(url_for('logged'))
  
  return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    
    conn.commit()
    conn.close()
    
    flash('Usuário criado com sucesso!')
    return redirect(url_for('index'))
  return render_template('register.html')

@app.route('/logged')
def logged():
    if session.get("username"):
        return render_template('logged.html')
    
    return redirect(url_for("login"))

def init_db():
  conn = sqlite3.connect('users.db')
  cursor = conn.cursor()
  cursor.execute('''
  CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  password TEXT NOT NULL
  )
  ''')
  conn.commit()
  conn.close()
init_db()

if __name__ == "__main__":
    app.run(debug=True)