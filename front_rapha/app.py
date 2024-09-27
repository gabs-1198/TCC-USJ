from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import uuid
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configurações da conexão MySQL
db = mysql.connector.connect(
    host="127.0.0.1",
    port=3005,
    user="root",
    password="",
    database="formulario_login"
)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form) 
        email = request.form.get['email']
        senha = request.form.get['senha']

        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM credenciais WHERE email = %s AND senha = %s"
        cursor.execute(query, (email, senha))
        user = cursor.fetchone()

    if not email or not senha:
        flash('Por favor, preencha todos os campos!', 'danger')
        return redirect(url_for('login'))

    if user and check_password_hash(user['senha'], senha):
        session['loggedin'] = True
        session['email'] = user['email']
        flash('Login bem-sucedido!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Usuário ou senha incorretos!', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        data_nasc = request.form['data_nasc']
        funcao = request.form['funcao']
        
        # Gerar ID de credencial única
        credencial_id = str(uuid.uuid4())

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM credenciais WHERE email = %s", (email,))
        account = cursor.fetchone()

        if account:
            flash('E-mail já cadastrado!', 'danger')
        else:
            hashed_password = generate_password_hash(senha)
            cursor.execute(
                "INSERT INTO credenciais (email, senha, nome, sobrenome, data_nasc, funcao, idcredenciais) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (email, hashed_password, nome, sobrenome, data_nasc, funcao, credencial_id)
            )
            db.commit()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        return f"Bem-vindo(a), {session['email']}!"
    else:
        return render_template('pagina-princial.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
