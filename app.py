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
    return redirect(url_for('register'))

  if session.get('username'):
    return redirect(url_for('logged'))
  
  return render_template('login.html')


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
    return redirect(url_for('login'))
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

#cadastro de aluno
alunos = []

@app.route('/listar-alunos')
def listar_alunos():
  if not session.get("username"):
    return redirect(url_for('login'))
  return render_template('listar_alunos.html', alunos=alunos)

@app.route('/adicionar-aluno', methods=['GET', 'POST'])
def adicionar_aluno():
    if not session.get("username"):
      return redirect(url_for('login'))
    
    if request.method == 'POST':
        matricula = request.form['matricula']
        NomeAluno = request.form['NomeAluno']

        aluno = {
                'NomeAluno': NomeAluno,
                'matricula': matricula
        }
        alunos.append(aluno)

        return redirect(url_for('listar_alunos'))
    return render_template('adicionar_alunos.html')

@app.route('/editar-alunos/<int:id>', methods=['GET', 'POST'])
def editar_aluno(id):
    if not session.get("username"):
      return redirect(url_for('login'))
    aluno = alunos[id]

    if request.method == 'POST':
        aluno['NomeAluno'] = request.form['NomeAluno']
        aluno['matricula'] = request.form['matricula']

        return redirect(url_for('listar_alunos'))
    return render_template('editar_alunos.html', id=id, aluno=aluno)

@app.route('/excluir-aluno/<int:id>', methods=['POST'])
def excluir_aluno(id):
    if not session.get("username"):
      return redirect(url_for('login'))
    del alunos[id]
    return redirect(url_for('listar_alunos'))


if __name__ == "__main__":
    app.run(debug=True)