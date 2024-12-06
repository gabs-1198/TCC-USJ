import datetime
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
        username = request.form['username']
        senha = request.form['senha']

        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM credenciais WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        # Verifica se o usuário existe e se a senha está correta
        if user:
            hashed_password = user['senha']
            if check_password_hash(hashed_password, senha):
                session['loggedin'] = True
                session['username'] = user['username']
                flash('Login bem-sucedido!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Senha incorreta!', 'danger')
        else:
            flash('Usuário não encontrado!', 'danger')
    
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
                "INSERT INTO credenciais (username, senha, nome, sobrenome, data_nasc, funcao, idcredenciais) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (username, hashed_password, nome, sobrenome, data_nasc, funcao, credencial_id)
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
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT carros.*, empresas.nome AS empresa_nome 
            FROM carros 
            JOIN empresas ON carros.empresa_id = empresas.id
        """)
        carros = cursor.fetchall()
        cursor.execute("SELECT * FROM empresas")
        empresas = cursor.fetchall()
        return render_template('pagina-principal.html', carros=carros, empresas=empresas)
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

        cursor = db.cursor()
        query = """
            UPDATE carros 
            SET modelo = %s, ano = %s, placa = %s, ultima_troca_pneus = %s, ultima_troca_oleo = %s, ultima_revisao = %s,
                ultima_troca_vela = %s, ultima_troca_caixa_cambio = %s, ultima_troca_suspensao = %s, 
                ultima_troca_bateria = %s, validade_bateria = %s, ultima_troca_correia_dentada = %s, proxima_revisao = %s
            WHERE chassi = %s
        """
        cursor.execute(query, (modelo, ano, placa, ultima_troca_pneus, ultima_troca_oleo, ultima_revisao, 
                               ultima_troca_vela, ultima_troca_caixa_cambio, ultima_troca_suspensao, 
                               ultima_troca_bateria, validade_bateria, ultima_troca_correia_dentada, proxima_revisao, chassi))
        db.commit()
        flash('Informações do carro atualizadas com sucesso!', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Ocorreu um erro ao atualizar as informações do carro: {e}', 'danger')
    finally:
        cursor.close()

    return redirect(url_for('pagina_principal'))

@app.route('/carros_por_empresa', methods=['GET', 'POST'])
def carros_por_empresa():
    if 'loggedin' in session:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM empresas")
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

        return render_template('cadastros.html', empresas=empresas, carros=carros)
    else:
        flash('Você precisa fazer login primeiro.', 'danger')
        return redirect(url_for('login'))

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
        proxima_revisao = (datetime.datetime.strptime(ultima_revisao, '%Y-%m-%d') + datetime.timedelta(days=180)).date()
        data_cadastro = datetime.date.today()

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM carros WHERE placa = %s", (placa,))
        carro = cursor.fetchone()

        if carro:
            flash('Placa já existe!', 'danger')
        else:
            cursor.execute(
                """INSERT INTO carros 
                (chassi, modelo, ano, placa, empresa_id, ultima_troca_pneus, ultima_troca_oleo, ultima_revisao, 
                ultima_troca_vela, ultima_troca_caixa_cambio, ultima_troca_suspensao, ultima_troca_bateria, 
                validade_bateria, ultima_troca_correia_dentada, proxima_revisao, data_cadastro) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (chassi, modelo, ano, placa, empresa_id, ultima_troca_pneus, ultima_troca_oleo, ultima_revisao, 
                ultima_troca_vela, ultima_troca_caixa_cambio, ultima_troca_suspensao, ultima_troca_bateria, 
                validade_bateria, ultima_troca_correia_dentada, proxima_revisao, data_cadastro)
            )
            db.commit()
            flash('Carro cadastrado com sucesso!', 'success')
        
        return redirect(url_for('pagina_principal'))
    else:
        flash('Você precisa fazer login primeiro.', 'danger')
        return redirect(url_for('login'))


@app.route('/data')
def get_data():
    year = request.args.get('year', type=int)
    
    cursor = db.cursor(dictionary=True)
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
    return jsonify(data)

@app.route('/available_years')
def get_available_years():
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT DISTINCT YEAR(data_cadastro) AS year FROM carros ORDER BY year
    """
    cursor.execute(query)
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/anotacoes', methods=['GET', 'POST'])
def anotacoes():
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
                "INSERT INTO anotacoes (placa, titulo, descricao, data_anotacao) VALUES (%s, %s, %s, %s)",
                (placa, titulo, descricao, data_anotacao)
            )
            db.commit()
            flash('Anotação salva com sucesso!', 'success')
            return redirect(url_for('anotacoes'))

        cursor.execute("SELECT * FROM anotacoes")
        anotacoes = cursor.fetchall()

        return render_template('anotacoes.html', carros=carros, anotacoes=anotacoes)
    else:
        flash('Por favor, faça login para continuar.', 'danger')
        return redirect(url_for('login'))

@app.route('/add_anotacao', methods=['POST'])
def add_anotacao():
    if 'loggedin' in session:
        placa = request.form['placa']
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        data_anotacao = datetime.date.today()

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO anotacoes (placa, titulo, descricao, data_anotacao) VALUES (%s, %s, %s, %s)",
            (placa, titulo, descricao, data_anotacao)
        )
        db.commit()
        flash('Anotação salva com sucesso!', 'success')
        return redirect(url_for('anotacoes'))
    else:
        flash('Por favor, faça login para continuar.', 'danger')
        return redirect(url_for('login'))

@app.route('/cadastros')
def cadastros():
    if 'loggedin' in session:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM empresas")
        empresas = cursor.fetchall()
        return render_template('cadastros.html', empresas=empresas)
    else:
        flash('Você precisa fazer login primeiro.', 'danger')
        return redirect(url_for('login'))
    
@app.route('/perfil')
def perfil():
    if 'loggedin' in session:
        return render_template('perfil.html')
    else:
        flash('Você precisa fazer login primeiro.', 'danger')
        return redirect(url_for('login'))

@app.route('/add_empresa', methods=['POST'])
def add_empresa():
    if 'loggedin' in session:
        nome = request.form['nome']
        responsavel = request.form['responsavel']
        estado = request.form['estado']
        cnpj = request.form['cnpj']
        telefone = request.form['telefone']
        username = request.form['username']

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO empresas (nome, responsavel, estado, cnpj, telefone, username) VALUES (%s, %s, %s, %s, %s, %s)",
            (nome, responsavel, estado, cnpj, telefone, username)
        )
        db.commit()
        flash('Perfil da empresa salvo com sucesso!', 'success')
        return redirect(url_for('perfil'))
    else:
        flash('Você precisa fazer login primeiro.', 'danger')
        return redirect(url_for('login'))

@app.route('/delete_anotacao/<int:id>', methods=['POST'])
def delete_anotacao(id):
    if 'loggedin' in session:
        cursor = db.cursor()
        cursor.execute("DELETE FROM anotacoes WHERE id = %s", (id,))
        db.commit()
        flash('Anotação excluída com sucesso!', 'success')
        return redirect(url_for('anotacoes'))
    else:
        flash('Por favor, faça login para continuar.', 'danger')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)