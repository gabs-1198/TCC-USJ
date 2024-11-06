from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
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
     return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM credenciais WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        # Verifica se o email existe e se a senha está correta
        if user:
            hashed_password = user['senha']
            if check_password_hash(hashed_password, senha):
                session['loggedin'] = True
                session['email'] = user['email']
                flash('Login bem-sucedido!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Senha incorreta!', 'danger')
        else:
            flash('Email não encontrado!', 'danger')
    
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
            # Criptografar a senha antes de salvar no banco de dados
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
        return redirect(url_for('pagina_principal'))
    else:
        flash('Você precisa fazer login primeiro.', 'danger')
        return redirect(url_for('login'))

@app.route('/pagina-principal')
def pagina_principal():
    if 'loggedin' in session:
        # Obter os carros do banco de dados
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM carros")
        carros = cursor.fetchall()  # Busca todos os carros
        
        # Passar os dados para o template
        return render_template('pagina-principal.html', carros=carros)
    else:
        flash('Por favor, faça login para continuar.', 'danger')
        return redirect(url_for('login'))


@app.route('/edit_car', methods=['POST'])
def edit_car():
    if 'loggedin' not in session:
        flash('Você precisa fazer login primeiro.', 'danger')
        return redirect(url_for('login'))

    try:
        chassi = request.form['chassi']
        modelo = request.form['modelo']
        ano = request.form['ano']
        ultima_troca_pneus = request.form['ultima_troca_pneus']
        ultima_troca_oleo = request.form['ultima_troca_oleo']
        ultima_revisao = request.form['ultima_revisao']

        cursor = db.cursor()
        query = """
            UPDATE carros 
            SET modelo = %s, ano = %s, ultima_troca_pneus = %s, ultima_troca_oleo = %s, ultima_revisao = %s 
            WHERE chassi = %s
        """
        cursor.execute(query, (modelo, ano, ultima_troca_pneus, ultima_troca_oleo, ultima_revisao, chassi))
        db.commit()
        flash('Informações do carro atualizadas com sucesso!', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Ocorreu um erro ao atualizar as informações do carro: {e}', 'danger')
    finally:
        cursor.close()

    return redirect(url_for('pagina_principal'))

# Função para cadastrar um novo carro
@app.route('/add_car', methods=['POST'])
def add_car():
    if request.method == 'POST':
        # Recebe dados do formulário de cadastro e insere no banco de dados
        chassi = request.form['chassi']
        modelo = request.form['modelo']
        ano = request.form['ano']
        ultima_troca_pneus = request.form['ultima_troca_pneus']
        ultima_troca_oleo = request.form['ultima_troca_oleo']
        ultima_revisao = request.form['ultima_revisao']

        cursor = db.cursor()
        query = """
            INSERT INTO carros (chassi, modelo, ano, ultima_troca_pneus, ultima_troca_oleo, ultima_revisao) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (chassi, modelo, ano, ultima_troca_pneus, ultima_troca_oleo, ultima_revisao))
        db.commit()
        flash('Carro cadastrado com sucesso!', 'success')
        return redirect(url_for('pagina_principal'))

@app.route('/data')
def get_data():
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)
    
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT 
            COUNT(ultima_troca_pneus) AS count, 
            'Pneus' AS type 
        FROM carros 
        WHERE MONTH(ultima_troca_pneus) = %s 
        AND YEAR(ultima_troca_pneus) = %s
        UNION ALL
        SELECT 
            COUNT(ultima_troca_oleo) AS count, 
            'Óleo' AS type 
        FROM carros 
        WHERE MONTH(ultima_troca_oleo) = %s 
        AND YEAR(ultima_troca_oleo) = %s
        UNION ALL
        SELECT 
            COUNT(ultima_revisao) AS count, 
            'Revisão' AS type 
        FROM carros 
        WHERE MONTH(ultima_revisao) = %s 
        AND YEAR(ultima_revisao) = %s
    """
    cursor.execute(query, (month, year, month, year, month, year))
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/available_dates')
def get_available_dates():
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT DISTINCT YEAR(ultima_troca_pneus) AS year, MONTH(ultima_troca_pneus) AS month FROM carros WHERE ultima_troca_pneus IS NOT NULL
        UNION
        SELECT DISTINCT YEAR(ultima_troca_oleo) AS year, MONTH(ultima_troca_oleo) AS month FROM carros WHERE ultima_troca_oleo IS NOT NULL
        UNION
        SELECT DISTINCT YEAR(ultima_revisao) AS year, MONTH(ultima_revisao) AS month FROM carros WHERE ultima_revisao IS NOT NULL
        ORDER BY year, month
    """
    cursor.execute(query)
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/available_years')
def get_available_years():
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT DISTINCT YEAR(ultima_troca_pneus) AS year FROM carros WHERE ultima_troca_pneus IS NOT NULL
        UNION
        SELECT DISTINCT YEAR(ultima_troca_oleo) AS year FROM carros WHERE ultima_troca_oleo IS NOT NULL
        UNION
        SELECT DISTINCT YEAR(ultima_revisao) AS year FROM carros WHERE ultima_revisao IS NOT NULL
        ORDER BY year
    """
    cursor.execute(query)
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/available_months')
def get_available_months():
    year = request.args.get('year', type=int)
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT DISTINCT MONTH(ultima_troca_pneus) AS month FROM carros WHERE YEAR(ultima_troca_pneus) = %s AND ultima_troca_pneus IS NOT NULL
        UNION
        SELECT DISTINCT MONTH(ultima_troca_oleo) AS month FROM carros WHERE YEAR(ultima_troca_oleo) = %s AND ultima_troca_oleo IS NOT NULL
        UNION
        SELECT DISTINCT MONTH(ultima_revisao) AS month FROM carros WHERE YEAR(ultima_revisao) = %s AND ultima_revisao IS NOT NULL
        ORDER BY month
    """
    cursor.execute(query, (year, year, year))
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)