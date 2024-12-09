import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import uuid
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)
LOGIN_REQUIRED_MESSAGE = 'Por favor, faça login para continuar.'
ANNOTATION_SAVED_SUCCESS_MESSAGE = 'Anotação salva com sucesso!'

# Configurações da conexão MySQL
db = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="",
    database="dados_tcc"
)

# SQL Queries
SELECT_ALL_EMPRESAS = "SELECT * FROM empresas"
INSERT_ANOTACOES = "INSERT INTO anotacoes (placa, titulo, descricao, data_anotacao) VALUES (%s, %s, %s, %s)"

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('loggedin') or not session.get('is_admin'):
            flash('Acesso negado: apenas administradores podem acessar esta página.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def cliente_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('loggedin') or session.get('is_admin'):
            flash('Acesso negado: apenas clientes podem acessar esta página.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
     return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']

        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM credenciais WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['senha'], senha):
            session['loggedin'] = True
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            flash('Login bem-sucedido!', 'success')
            if user['is_admin']:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard_user'))
        else:
            flash('Usuário ou senha incorretos!', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        data_nasc = request.form['data_nasc']
        funcao = request.form['funcao']
        is_admin = request.form['is_admin'] == '1'
        
        empresa_id = request.form.get('empresa_id') if not is_admin else None
        
        # Gerar ID de credencial única
        credencial_id = str(uuid.uuid4())

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM credenciais WHERE username = %s", (username,))
        account = cursor.fetchone()

        if account:
            flash('Usuário já cadastrado!', 'danger')
        else:
            # Criptografar a senha antes de salvar no banco de dados
            hashed_password = generate_password_hash(senha)
            cursor.execute(
                "INSERT INTO credenciais (username, senha, nome, sobrenome, data_nasc, funcao, empresa_id, is_admin, idcredenciais) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (username, hashed_password, nome, sobrenome, data_nasc, funcao, empresa_id, is_admin, credencial_id)
            )
            db.commit()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        cursor.execute(SELECT_ALL_EMPRESAS)
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(SELECT_ALL_EMPRESAS)
    finally:
        cursor.close()
@app.route('/admin_dashboard')
@admin_required
def admin_dashboard():
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT carros.*, empresas.nome AS empresa_nome 
            FROM carros 
            JOIN empresas ON carros.empresa_id = empresas.id
        """)
        carros = cursor.fetchall()
        cursor.execute(SELECT_ALL_EMPRESAS)
        empresas = cursor.fetchall()
        return render_template('dashboard_admin.html', carros=carros, empresas=empresas)
    finally:
        cursor.close()

@app.route('/dashboard_user')
def dashboard_user():
    if 'loggedin' in session:
        return render_template('dashboard_user.html')
    else:
        flash(LOGIN_REQUIRED_MESSAGE, 'danger')
        return redirect(url_for('login'))

@app.route('/cliente_dashboard')
@cliente_required
def cliente_dashboard():
    return render_template('dashboard_user.html')

@app.route('/edit_car', methods=['POST'])
def edit_car():
    if 'loggedin' not in session:
        flash(LOGIN_REQUIRED_MESSAGE, 'danger')
        return redirect(url_for('login'))

    try:
        chassi = request.form['chassi']
        modelo = request.form['modelo']
        ano = request.form['ano']
        placa = request.form['placa']
        ultima_troca_pneus = request.form['ultima_troca_pneus']
        ultima_troca_oleo = request.form['ultima_troca_oleo']
        ultima_revisao = request.form['ultima_revisao']
        ultima_troca_vela = request.form['ultima_troca_vela']
        ultima_troca_caixa_cambio = request.form['ultima_troca_caixa_cambio']
        ultima_troca_suspensao = request.form['ultima_troca_suspensao']
        ultima_troca_bateria = request.form['ultima_troca_bateria']
        validade_bateria = request.form['validade_bateria']
        ultima_troca_correia_dentada = request.form['ultima_troca_correia_dentada']
        proxima_revisao = (datetime.datetime.strptime(ultima_revisao, '%Y-%m-%d') + datetime.timedelta(days=180)).date()
        scanner_instalado = request.form['scanner_instalado']

        cursor = db.cursor()
        query = """
            UPDATE carros 
            SET modelo = %s, ano = %s, placa = %s, ultima_troca_pneus = %s, ultima_troca_oleo = %s, ultima_revisao = %s,
                ultima_troca_vela = %s, ultima_troca_caixa_cambio = %s, ultima_troca_suspensao = %s, 
                ultima_troca_bateria = %s, validade_bateria = %s, ultima_troca_correia_dentada = %s, proxima_revisao = %s,
                scanner_instalado = %s
            WHERE chassi = %s
        """
        cursor.execute(query, (modelo, ano, placa, ultima_troca_pneus, ultima_troca_oleo, ultima_revisao, 
                               ultima_troca_vela, ultima_troca_caixa_cambio, ultima_troca_suspensao, 
                               ultima_troca_bateria, validade_bateria, ultima_troca_correia_dentada, proxima_revisao,
                               scanner_instalado, chassi))
        db.commit()
        flash('Informações do carro atualizadas com sucesso!', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Ocorreu um erro ao atualizar as informações do carro: {e}', 'danger')
    finally:
        cursor.close()

    return redirect(url_for('cadastros_admin'))

# Função para cadastrar um novo carro
@app.route('/add_car', methods=['POST'])
def add_car():
    if 'loggedin' in session:
        chassi = request.form['chassi']
        modelo = request.form['modelo']
        ano = request.form['ano']
        placa = request.form['placa']
        empresa_id = request.form['empresa_id']
        ultima_troca_pneus = request.form['ultima_troca_pneus']
        ultima_troca_oleo = request.form['ultima_troca_oleo']
        ultima_revisao = request.form['ultima_revisao']
        ultima_troca_vela = request.form['ultima_troca_vela']
        ultima_troca_caixa_cambio = request.form['ultima_troca_caixa_cambio']
        ultima_troca_suspensao = request.form['ultima_troca_suspensao']
        ultima_troca_bateria = request.form['ultima_troca_bateria']
        validade_bateria = request.form['validade_bateria']
        ultima_troca_correia_dentada = request.form['ultima_troca_correia_dentada']
        proxima_revisao = request.form['proxima_revisao']
        scanner_instalado = request.form['scanner_instalado']
        data_cadastro = datetime.date.today()  # Adiciona a data de cadastro

        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM carros WHERE placa = %s", (placa,))
            carro = cursor.fetchone()

            if carro:
                flash('Placa já existe!', 'danger')
            else:
                cursor.execute(
                    """INSERT INTO carros 
                    (chassi, modelo, ano, placa, empresa_id, ultima_troca_pneus, ultima_troca_oleo, ultima_revisao, 
                    ultima_troca_vela, ultima_troca_caixa_cambio, ultima_troca_suspensao, ultima_troca_bateria, 
                    validade_bateria, ultima_troca_correia_dentada, proxima_revisao, scanner_instalado, data_cadastro) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (chassi, modelo, ano, placa, empresa_id, ultima_troca_pneus, ultima_troca_oleo, ultima_revisao, 
                    ultima_troca_vela, ultima_troca_caixa_cambio, ultima_troca_suspensao, ultima_troca_bateria, 
                    validade_bateria, ultima_troca_correia_dentada, proxima_revisao, scanner_instalado, data_cadastro)
                )
                db.commit()
                flash('Carro cadastrado com sucesso!', 'success')
        except Exception as e:
            db.rollback()
            flash(f'Ocorreu um erro ao cadastrar o carro: {e}', 'danger')
        finally:
            cursor.close()

        return redirect(url_for('cadastros_admin'))
    else:
        flash(LOGIN_REQUIRED_MESSAGE, 'danger')
        return redirect(url_for('login'))
    
@app.route('/data', methods=['GET'])
def get_data():
    year = request.args.get('year', type=int)
    
    cursor = db.cursor(dictionary=True)
    try:
        query = """
            SELECT 
                MONTH(data_cadastro) AS month, 
                COUNT(*) AS count 
            FROM carros 
            WHERE YEAR(data_cadastro) = %s 
            GROUP BY MONTH(data_cadastro)
            ORDER BY MONTH(data_cadastro)
        """
        cursor.execute(query, (year,))
        data = cursor.fetchall()
    except Exception as e:
        flash(f'Ocorreu um erro ao buscar os dados: {e}', 'danger')
        data = []
    finally:
        cursor.close()
    
    return jsonify(data)

@app.route('/anotacoes_admin', methods=['GET', 'POST'])
@admin_required
def anotacoes_admin():
    if 'loggedin' in session:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM carros")
        carros = cursor.fetchall()

        if request.method == 'POST':
            placa = request.form['placa']
            titulo = request.form['titulo']
            descricao = request.form['descricao']
            data_anotacao = datetime.date.today()

            cursor.execute(
                INSERT_ANOTACOES,
                (placa, titulo, descricao, data_anotacao)
            )
            db.commit()
            flash(ANNOTATION_SAVED_SUCCESS_MESSAGE, 'success')
            return redirect(url_for('anotacoes_admin'))

        cursor.execute("SELECT * FROM anotacoes")
        anotacoes = cursor.fetchall()
        cursor.close()

        return render_template('anotacoes_admin.html', carros=carros, anotacoes=anotacoes)
    else:
        flash(LOGIN_REQUIRED_MESSAGE, 'danger')
        return redirect(url_for('login'))

@app.route('/add_anotacao', methods=['POST'])
def add_anotacao():
    if 'loggedin' in session:
        placa = request.form['placa']
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        data_anotacao = request.form['data_anotacao']
        cursor = db.cursor()
        try:
            cursor.execute(
                INSERT_ANOTACOES,
                (placa, titulo, descricao, data_anotacao)
            )
            db.commit()
            flash(ANNOTATION_SAVED_SUCCESS_MESSAGE, 'success')
        finally:
            cursor.close()
        db.commit()
        flash(ANNOTATION_SAVED_SUCCESS_MESSAGE, 'success')
        return render_template('anotacoes_admin.html', carros=carros, anotacoes=anotacoes)
    else:
        flash(LOGIN_REQUIRED_MESSAGE, 'danger')
        return redirect(url_for('login'))

@app.route('/anotacoes_usuario')
def anotacoes_usuario():
    if 'loggedin' in session:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT empresa_id FROM credenciais WHERE username = %s", (session['username'],))
        user = cursor.fetchone()
        empresa_id = user['empresa_id']

        cursor.execute("SELECT * FROM carros WHERE empresa_id = %s", (empresa_id,))
        carros = cursor.fetchall()

        cursor.execute("SELECT * FROM anotacoes WHERE placa IN (SELECT placa FROM carros WHERE empresa_id = %s)", (empresa_id,))
        anotacoes = cursor.fetchall()

        return render_template('anotacoes_usuario.html', carros=carros, anotacoes=anotacoes)
    else:
        flash(LOGIN_REQUIRED_MESSAGE, 'danger')
        return redirect(url_for('login'))

@app.route('/add_anotacao_usuario', methods=['POST'])
def add_anotacao_usuario():
    if 'loggedin' in session:
        placa = request.form['placa']
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        data_anotacao = datetime.date.today()

        cursor = db.cursor()
        cursor.execute("SELECT empresa_id FROM carros WHERE placa = %s", (placa,))
        carro = cursor.fetchone()

        cursor.execute("SELECT empresa_id FROM credenciais WHERE username = %s", (session['username'],))
        user = cursor.fetchone()

        if carro and user and carro['empresa_id'] == user['empresa_id']:
            cursor.execute(
                INSERT_ANOTACOES,
                (placa, titulo, descricao, data_anotacao)
            )
            db.commit()
            flash(ANNOTATION_SAVED_SUCCESS_MESSAGE, 'success')
        else:
            flash('Você só pode fazer anotações em carros da sua própria empresa.', 'danger')

        return redirect(url_for('anotacoes_usuario'))
    else:
        flash(LOGIN_REQUIRED_MESSAGE, 'danger')
        return redirect(url_for('login'))
    
@app.route('/criar_perfil', methods=['GET', 'POST'])
@admin_required
def criar_perfil():
    if 'loggedin' in session:
        if request.method == 'POST':
            nome = request.form['nome']
            responsavel = request.form['responsavel']
            estado = request.form['estado']
            cnpj = request.form['cnpj']
            telefone = request.form['telefone']

            cursor = db.cursor()
            try:
                cursor.execute(
                    "INSERT INTO empresas (nome, responsavel, estado, cnpj, telefone) VALUES (%s, %s, %s, %s, %s)",
                    (nome, responsavel, estado, cnpj, telefone)
                )
                db.commit()
                flash('Perfil da empresa criado com sucesso!', 'success')
                return redirect(url_for('admin_dashboard'))
            finally:
                cursor.close()

        return render_template('criar_perfil.html')
    else:
        flash(LOGIN_REQUIRED_MESSAGE, 'danger')
        return redirect(url_for('login'))

@app.route('/delete_anotacao/<int:id>', methods=['POST'])
def delete_anotacao(id):
    if 'loggedin' in session:
        cursor = db.cursor()
        cursor.execute("DELETE FROM anotacoes WHERE id = %s", (id,))
        db.commit()
        flash('Anotação excluída com sucesso!', 'success')
        return redirect(url_for('anotacoes_admin'))
    else:
        flash(LOGIN_REQUIRED_MESSAGE, 'danger')
        return redirect(url_for('login'))

@app.route('/ver_perfil')
def ver_perfil():
    if 'loggedin' in session:
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT empresas.* 
            FROM empresas 
            JOIN credenciais ON empresas.id = credenciais.empresa_id 
            WHERE credenciais.username = %s
        """, (session['username'],))
        empresa = cursor.fetchone()
        return render_template('ver_perfil.html', empresa=empresa)
    else:
        flash(LOGIN_REQUIRED_MESSAGE, 'danger')
        return redirect(url_for('login'))

@app.route('/visualizar_cadastros', methods=['GET', 'POST'])
def visualizar_cadastros():
    if 'loggedin' in session:
        cursor = db.cursor(dictionary=True)
        cursor.execute(SELECT_ALL_EMPRESAS)
        empresas = cursor.fetchall()

        carros = []
        if request.method == 'POST':
            empresa_id = request.form['empresa_id']
            cursor.execute("""
                SELECT chassi, modelo, ano, placa, ultima_revisao, 
                       DATE_ADD(ultima_revisao, INTERVAL 6 MONTH) AS proxima_revisao,
                       ultima_troca_pneus, ultima_troca_oleo, ultima_troca_vela, 
                       ultima_troca_caixa_cambio, ultima_troca_suspensao, 
                       ultima_troca_bateria, validade_bateria, ultima_troca_correia_dentada
                FROM carros 
                WHERE empresa_id = %s
            """, (empresa_id,))
            carros = cursor.fetchall()

        return render_template('visualizar_cadastros.html', empresas=empresas, carros=carros)
    else:
        flash(LOGIN_REQUIRED_MESSAGE, 'danger')
        return redirect(url_for('login'))

@app.route('/solicitar_modificacao', methods=['POST'])
def solicitar_modificacao():
    if 'loggedin' in session:
        chassi = request.form['chassi']
        campo = request.form['campo']
        novo_valor = request.form['novo_valor']

        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO solicitacoes_modificacao (chassi, campo, novo_valor, data_solicitacao) VALUES (%s, %s, %s, %s)",
                (chassi, campo, novo_valor, datetime.datetime.now())
            )
            db.commit()
            flash('Solicitação de modificação enviada com sucesso!', 'success')
        finally:
            cursor.close()
        return redirect(url_for('visualizar_cadastros'))
    else:
        flash(LOGIN_REQUIRED_MESSAGE, 'danger')
        return redirect(url_for('login'))

@app.route('/cadastros_admin', methods=['GET', 'POST'])
@admin_required
def cadastros_admin():
    if 'loggedin' in session:
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute(SELECT_ALL_EMPRESAS)
            empresas = cursor.fetchall()

            carros = []
            if request.method == 'POST':
                empresa_id = request.form['empresa_id']
                cursor.execute("""
                    SELECT chassi, modelo, ano, placa, ultima_revisao, 
                           DATE_ADD(ultima_revisao, INTERVAL 6 MONTH) AS proxima_revisao,
                           ultima_troca_pneus, ultima_troca_oleo, ultima_troca_vela, 
                           ultima_troca_caixa_cambio, ultima_troca_suspensao, 
                           ultima_troca_bateria, validade_bateria, ultima_troca_correia_dentada, scanner_instalado
                    FROM carros 
                    WHERE empresa_id = %s
                """, (empresa_id,))
                carros = cursor.fetchall()

            return render_template('cadastros_admin.html', empresas=empresas, carros=carros)
        finally:
            cursor.close()
    else:
        flash('Você precisa fazer login primeiro.', 'danger')
        return redirect(url_for('login'))

@app.route('/available_years', methods=['GET'])
def available_years():
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT DISTINCT YEAR(data_cadastro) AS year FROM carros ORDER BY year")
        years = cursor.fetchall()
    except Exception as e:
        flash(f'Ocorreu um erro ao buscar os anos disponíveis: {e}', 'danger')
        years = []
    finally:
        cursor.close()
    
    return jsonify(years)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)